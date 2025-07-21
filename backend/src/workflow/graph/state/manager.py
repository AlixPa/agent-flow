import asyncio
import json
from logging import Logger

from src.clients import AMysqlClientReader, AMysqlClientWriter
from src.logger import get_logger
from src.models.database import (
    ConversationTable,
    GraphStateTable,
    GraphTable,
    NodeTable,
    UserTable,
)

from .models import GraphState, MessageHistory

logger = get_logger()


class StateManager:
    def __init__(
        self,
        logger: Logger = logger,
        silent: bool = False,
    ) -> None:
        self.logger = logger
        self.mysql_reader = AMysqlClientReader(logger=logger)
        self.mysql_writer = AMysqlClientWriter(logger=logger)

    async def load_state(self, id: str) -> GraphState:
        graph_state_db = await self.mysql_reader.select_by_id(
            table=GraphStateTable, id=id
        )
        message_history = MessageHistory(**json.loads(graph_state_db.message_history))

        conversation_task = self.mysql_reader.select_by_id(
            table=ConversationTable, id=graph_state_db.conversationId
        )
        graph_task = self.mysql_reader.select_by_id(
            table=GraphTable, id=graph_state_db.graphId
        )
        entry_node_task = self.mysql_reader.select_by_id(
            table=NodeTable, id=graph_state_db.entryNodeId
        )
        user_task = self.mysql_reader.select_by_id(
            table=UserTable, id=graph_state_db.userId
        )
        conversation, graph, entry_node, user = await asyncio.gather(
            conversation_task,
            graph_task,
            entry_node_task,
            user_task,
        )
        return GraphState(
            message_history=message_history,
            conversation=conversation,
            entry_node=entry_node,
            graph=graph,
            user=user,
        )

    async def save_state(self, state: GraphState) -> str:
        graph_state_db = GraphStateTable(
            message_history=state.message_history.model_dump_json(),
            conversationId=state.conversation.id,
            entryNodeId=state.entry_node.id,
            graphId=state.graph.id,
            userId=state.user.id,
        )
        await self.mysql_writer.insert_one(
            table=GraphStateTable, to_insert=graph_state_db
        )
        return graph_state_db.id
