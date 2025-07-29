from logging import Logger
from typing import Any, Callable, Coroutine

from langgraph.graph import StateGraph
from langgraph.graph.state import CompiledStateGraph
from src.agents.base import BaseAgent
from src.clients.mysql import AMysqlClientReader
from src.config.default_db_settings import DefaultDbSettings
from src.logger import get_logger
from src.models.database import AgentNodeTable, EdgeTable, NodeTable
from src.workflow.graph.state import GraphState

from .config import BuilderConfig
from .exceptions import NoAgentNodeId

base_logger = get_logger()


class GraphBuilder:
    def __init__(
        self,
        logger: Logger | None = None,
    ) -> None:
        self.logger = logger or base_logger
        self.mysql_client = AMysqlClientReader(logger=self.logger)

    async def _load_nodes(self, graph_id: str) -> list[NodeTable]:
        nodes = await self.mysql_client.select(
            table=NodeTable,
            cond_equal={"graphId": graph_id},
        )
        self.logger.debug(f"Loaded nodes from {graph_id=}. {nodes=}")
        return nodes

    async def _load_edges(self, graph_id: str) -> list[EdgeTable]:
        edges = await self.mysql_client.select(
            table=EdgeTable,
            cond_equal={"graphId": graph_id},
        )
        self.logger.debug(f"Loaded edges from {graph_id=}. {edges=}")
        return edges

    async def _load_agent_node(self, id: str) -> AgentNodeTable:
        agent_node = await self.mysql_client.select_by_id(
            table=AgentNodeTable,
            id=id,
        )
        self.logger.debug(f"Loaded agent_node of {id=}. {agent_node=}")
        return agent_node

    def _get_agent(self, agent_node: AgentNodeTable) -> BaseAgent:
        agent_class = BuilderConfig.map_name_agent[agent_node.agentBaseName]
        agent = agent_class(
            model=agent_node.customModel,
            system_prompt=agent_node.customPrompt,
            name=agent_node.agentBaseName,
            logger=self.logger,
        )
        self.logger.debug(f"Constructed agent for {agent_node=}")
        return agent

    async def _get_step(
        self,
        node: NodeTable,
    ) -> Callable[[GraphState], Coroutine[Any, Any, GraphState]]:
        if node.type == "agent":
            if not node.agentNodeId:
                raise NoAgentNodeId
            agent_node = await self._load_agent_node(id=node.agentNodeId)
            agent_model = self._get_agent(agent_node=agent_node)
            step = BuilderConfig.map_name_step_with_agent[agent_node.agentBaseName](
                agent_model, node
            )
        else:
            step = BuilderConfig.map_name_step_no_agent[node.type](node)
        self.logger.debug(f"Got step for {node=}")
        return step

    async def get_graph(
        self,
        id: str,
        state: GraphState,
    ) -> CompiledStateGraph:
        self.logger.info(f"Building graph of {id=}.")
        builder = StateGraph(GraphState)

        for node in await self._load_nodes(graph_id=id):
            self.logger.debug(f"adding to the graph, {node=}")

            step = await self._get_step(node=node)
            builder.add_node(node.id, step)

            # Use the base entry point on the first ever step on the graph.
            if state.entry_node.id == DefaultDbSettings.NODE.id:
                if node.isBaseEntryPoint:
                    self.logger.info(f"Entry point is {node=}")
                    builder.set_entry_point(node.id)
                    state.entry_node = node
            elif node.id == state.entry_node.id:
                self.logger.info(f"Entry point is {node=}")
                builder.set_entry_point(node.id)

        for edge in await self._load_edges(graph_id=id):
            self.logger.debug(f"adding to the graph, {edge=}")
            builder.add_edge(edge.fromNodeId, edge.toNodeId)

        graph = builder.compile()
        self.logger.info(f"Successfuly built the graph of {id=}")
        return graph
