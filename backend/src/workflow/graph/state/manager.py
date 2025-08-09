import asyncio
import json
from logging import Logger

from src.clients.messenger import Messenger
from src.clients.mysql import AMysqlClientReader, AMysqlClientWriter
from src.logger import get_logger
from src.models.database import (
    ConversationTable,
    GraphStateTable,
    GraphTable,
    NodeTable,
    UserTable,
)

from .models import GraphState, MessageHistory

base_logger = get_logger()


class StateManager:
    def __init__(
        self,
        logger: Logger | None = None,
    ) -> None:
        self.logger = logger or base_logger
        self.mysql_reader = AMysqlClientReader(logger=self.logger)
        self.mysql_writer = AMysqlClientWriter(logger=self.logger)

    async def load_state(
        self,
        state_id: str,
        skip_next_input: bool = True,
        stop_execution: bool = False,
    ) -> GraphState:
        self.logger.debug(
            f"Loading state in manager with {state_id=}, {skip_next_input=}, {stop_execution=}."
        )
        graph_state_db = await self.mysql_reader.select_by_id(
            table=GraphStateTable,
            id=state_id,
        )
        message_history = MessageHistory(**json.loads(graph_state_db.message_history))

        conversation_task = self.mysql_reader.select_by_id(
            table=ConversationTable,
            id=graph_state_db.conversationId,
        )
        graph_task = self.mysql_reader.select_by_id(
            table=GraphTable,
            id=graph_state_db.graphId,
        )
        entry_node_task = self.mysql_reader.select_by_id(
            table=NodeTable,
            id=graph_state_db.entryNodeId,
        )
        user_task = self.mysql_reader.select_by_id(
            table=UserTable,
            id=graph_state_db.userId,
        )
        conversation, graph, entry_node, user = await asyncio.gather(
            conversation_task,
            graph_task,
            entry_node_task,
            user_task,
        )
        state = GraphState(
            message_history=message_history,
            conversation=conversation,
            entry_node=entry_node,
            graph=graph,
            user=user,
            messenger=Messenger(),
            skip_next_input=skip_next_input,
            stop_execution=stop_execution,
        )
        self.logger.debug(f"Loaded state in manager, {state=}")
        return state

    async def save_state(self, state: GraphState) -> str:
        self.logger.debug(f"Saving state in manager {state=}")
        graph_state_db = GraphStateTable(
            message_history=state.message_history.model_dump_json(),
            conversationId=state.conversation.id,
            entryNodeId=state.entry_node.id,
            graphId=state.graph.id,
            userId=state.user.id,
        )
        await self.mysql_writer.insert_one(
            table=GraphStateTable,
            to_insert=graph_state_db,
        )
        self.logger.debug(f"Saved state in manager, {graph_state_db.id=}")
        return graph_state_db.id
