import asyncio
import traceback

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from src.clients.messenger import Messenger, StreamMessage
from src.clients.mysql import (
    AMysqlClientReader,
    AMysqlClientWriter,
    AMySqlIdNotFoundError,
)
from src.config.default_db_settings import DefaultDbSettings
from src.exceptions.http import HTTPWrongAttributesException
from src.logger import get_logger
from src.models.database import ConversationTable, GraphTable, UserTable
from src.workflow.graph.builder import GraphBuilder
from src.workflow.graph.state import ConversationMessage, GraphState, StateManager

from .models import ConversationRequest
from .service import load_row_from_db

router = APIRouter(prefix="/conversation")
logger = get_logger()


@router.post("/stream")
async def stream_conversation(req: ConversationRequest) -> StreamingResponse:
    logger.info(f"On POST /conversation/stream_conversation got {req=}")
    graph_builder = GraphBuilder(logger)
    state_manager = StateManager(logger)
    mysql_reader = AMysqlClientReader(logger)

    # TODO: Implement real user id
    if req.user_id is None:
        req.user_id = DefaultDbSettings.USER.id

    if req.state_id:
        # Continue an existing conversation, meaning a user message must be present
        if not req.user_message:
            raise HTTPWrongAttributesException("state_id found but not user_message.")
        try:
            start_state = await state_manager.load_state(id=req.state_id)
        except AMySqlIdNotFoundError:
            logger.error(
                f"Got requested with {req.state_id=}, but not existing. {traceback.format_exc()}"
            )
            raise HTTPWrongAttributesException(
                "no state founded with the state_id provided."
            )
        start_state.message_history.messages.append(
            ConversationMessage(speaker=start_state.user.name, text=req.user_message)
        )
    else:
        # Init the conversation, meaning a user message cannot be present at start
        if req.user_message:
            raise HTTPWrongAttributesException("user_message found but not state_id.")
        user = await load_row_from_db(table=UserTable, id=req.user_id, logger=logger)
        graph = await load_row_from_db(table=GraphTable, id=req.graph_id, logger=logger)
        try:
            conversation = await mysql_reader.select_by_id(
                table=ConversationTable, id=req.conversation_id
            )
        except AMySqlIdNotFoundError:
            logger.info(
                f"No conversation found with the id provided {req.conversation_id}, will create one in the database."
            )
            conversation = ConversationTable(graphId=req.graph_id, userId=req.user_id)
            mysql_writer = AMysqlClientWriter(logger)
            await mysql_writer.insert_one(
                table=ConversationTable, to_insert=conversation
            )
        start_state = GraphState(
            messenger=Messenger(logger),
            conversation=conversation,
            user=user,
            graph=graph,
        )
    logger.info(f"On POST /conversation/stream_conversation loaded {start_state=}")
    graph = await graph_builder.get_graph(id=req.graph_id, state=start_state)
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

    return StreamingResponse(
        start_state.messenger.stream(),
        media_type="text/event-stream",
    )
