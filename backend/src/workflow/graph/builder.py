from logging import Logger
from typing import Any, Callable, Coroutine, overload

from langgraph.graph import StateGraph
from langgraph.graph.state import CompiledStateGraph
from src.agents.base import BaseAgent
from src.agents.step_agents import ConversationalAgent
from src.clients import AMysqlClientReader
from src.logger import get_logger
from src.models.database import AgentNodeTable, EdgeTable, NodeTable

from .builder_config import BuilderConfig
from .graph_state import GraphState

logger = get_logger()


class GraphBuilder:
    def __init__(
        self,
        logger: Logger = logger,
        silent: bool = False,
    ) -> None:
        self.mysql_client = AMysqlClientReader()
        self.logger = logger
        self.silent = silent

    async def _load_nodes(self, graph_id: str) -> list[NodeTable]:
        return await self.mysql_client.select(
            table=NodeTable,
            cond_equal={"graphId": graph_id},
            silent=self.silent,
        )

    async def _load_edges(self, graph_id: str) -> list[EdgeTable]:
        return await self.mysql_client.select(
            table=EdgeTable,
            cond_equal={"graphId": graph_id},
            silent=self.silent,
        )

    async def _load_agent_node(self, id: str) -> AgentNodeTable:
        return await self.mysql_client.select_by_id(
            table=AgentNodeTable,
            id=id,
            silent=self.silent,
        )

    def _get_agent(self, agent_node: AgentNodeTable) -> BaseAgent:
        agent_class = BuilderConfig.map_name_agent[agent_node.agentBaseName]
        return agent_class(
            model=agent_node.customModel,
            system_prompt=agent_node.customPrompt,
        )

    @overload
    def _get_step(
        self, node: NodeTable
    ) -> Callable[[GraphState], Coroutine[Any, Any, GraphState]]: ...

    @overload
    def _get_step(
        self, node: AgentNodeTable
    ) -> Callable[[GraphState], Coroutine[Any, Any, GraphState]]: ...

    def _get_step(
        self,
        node: NodeTable | AgentNodeTable,
    ) -> Callable[[GraphState], Coroutine[Any, Any, GraphState]]:
        if isinstance(node, NodeTable):
            return BuilderConfig.map_name_step_no_agent[node.type]()
        else:
            agent = self._get_agent(agent_node=node)
            return BuilderConfig.map_name_step_with_agent[node.agentBaseName](agent)

    async def get_graph(self, id: str) -> CompiledStateGraph:
        self.logger.info(f"Building graph of {id=}.")
        builder = StateGraph(GraphState)

        for node in await self._load_nodes(graph_id=id):
            if not self.silent:
                self.logger.debug(f"adding to the graph, {node=}")
            if node.type == "agent":
                agent_node = await self._load_agent_node(id=node.agentNodeId)
                builder.add_node(node.id, self._get_step(node=agent_node))
            else:
                builder.add_node(node.id, self._get_step(node=node))

            if node.isBaseEntryPoint:
                builder.set_entry_point(node.id)

        for edge in await self._load_edges(graph_id=id):
            if not self.silent:
                self.logger.debug(f"adding to the graph, {edge=}")
            builder.add_edge(edge.fromNodeId, edge.toNodeId)

        graph = builder.compile()
        self.logger.info(f"Successfuly built the graph of {id=}")
        return graph
