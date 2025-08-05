import asyncio
import traceback
from logging import Logger
from typing import AsyncGenerator, Type, TypeVar

from src.clients.messenger import Messenger, StreamMessage
from src.clients.mysql import (
    AMysqlClientReader,
    AMysqlClientWriter,
    AMySqlIdNotFoundError,
)
from src.logger import get_logger
from src.models.database import BaseTableModel, ConversationTable, GraphTable, UserTable
from src.workflow.graph.builder import GraphBuilder
from src.workflow.graph.state import ConversationMessage, GraphState, StateManager

from .models import WrongArgumentException

logger = get_logger()

GenericTableModel = TypeVar("GenericTableModel", bound=BaseTableModel)


async def _load_row_from_db(
    table: Type[GenericTableModel], id: str, logger: Logger
) -> GenericTableModel:
    mysql_reader = AMysqlClientReader(logger)
    try:
        row = await mysql_reader.select_by_id(table=table, id=id)
    except AMySqlIdNotFoundError:
        logger.error(
            f"Failed to load {table.__tablename__} in load_row_from_db, {id=} is not existing."
        )
        raise WrongArgumentException(
            f"no {table.__tablename__} founded with the {table.__tablename__}_id provided."
        )
    return row


async def start_state_existing_conv(state_id: str, user_message: str) -> GraphState:
    state_manager = StateManager(logger)
    try:
        start_state = await state_manager.load_state(id=state_id)
    except AMySqlIdNotFoundError:
        logger.warning(
            f"Got requested with {state_id=}, but not existing. {traceback.format_exc()}"
        )
        raise WrongArgumentException("no state founded with the state_id provided.")
    start_state.message_history.messages.append(
        ConversationMessage(speaker=start_state.user.name, text=user_message)
    )
    return start_state


async def start_state_new_conv(user_id: str, graph_id: str, conversation_id: str):
    user = await _load_row_from_db(table=UserTable, id=user_id, logger=logger)
    graph = await _load_row_from_db(table=GraphTable, id=graph_id, logger=logger)

    if graph.userId != user.id:
        raise WrongArgumentException(
            f"Could not find the graph of id {graph_id} under the user of id {user_id}."
        )

    mysql_reader = AMysqlClientReader(logger)
    conversation_exists = await mysql_reader.id_exists(
        table=ConversationTable, id=conversation_id
    )
    if conversation_exists:
        raise WrongArgumentException(
            f"Found a conversation with id {conversation_id} but the request had no state_id nor user_message"
        )

    logger.info(
        f"No conversation found with the id provided {conversation_id}, will create one in the database."
    )
    conversation = ConversationTable(
        id=conversation_id, graphId=graph_id, userId=user_id
    )
    mysql_writer = AMysqlClientWriter(logger)
    await mysql_writer.insert_one(table=ConversationTable, to_insert=conversation)

    return GraphState(
        messenger=Messenger(logger),
        conversation=conversation,
        user=user,
        graph=graph,
    )


async def get_stream_flow(
    graph_id: str, start_state: GraphState
) -> AsyncGenerator[str, None]:
    graph_builder = GraphBuilder(logger)
    state_manager = StateManager(logger)

    graph = await graph_builder.get_graph(id=graph_id, state=start_state)
    iterator = graph.astream(start_state)

    async def iterate_graph():
        while True:
            step = await anext(iterator)
            executed_node = [k for k in step][0]
            state = GraphState(**step[executed_node])
            logger.info(
                f"On POST /conversation/stream_conversation, iterating the graph, now is {state=}"
            )

            if state.stop_execution:
                state_db_id = await state_manager.save_state(state=state)
                await state.messenger.send(
                    StreamMessage(
                        is_final_message=True,
                        state_id=state_db_id,
                        conversation_id=state.conversation.id,
                    )
                )
                break

    asyncio.create_task(iterate_graph())
    return start_state.messenger.stream()
