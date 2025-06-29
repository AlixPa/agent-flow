from _clients import MysqlClient
from _logger import get_logger
from _models import AgentBaseTable, AgentNodeTable, EdgeTable, NodeTable
from langgraph.graph import StateGraph
from langgraph.graph.state import CompiledStateGraph

from .graph_state import GraphState
from .maps import agent_base_name_class_map, node_type_step_func_map

logger = get_logger()


class GraphBuilder:
    def __init__(self) -> None:
        self.mysql_client = MysqlClient()
        self.agent_base_name_class_map = agent_base_name_class_map
        self.node_type_step_func_map = node_type_step_func_map

    def _get_nodes(self, graph_id: str) -> list[NodeTable]:
        return list(
            self.mysql_client.select(
                table=NodeTable,
                cond_equal={"graphId": graph_id},
            )
        )

    def _get_edges(self, graph_id: str) -> list[EdgeTable]:
        return list(
            self.mysql_client.select(
                table=EdgeTable,
                cond_equal={"graphId": graph_id},
            )
        )

    def _get_agent_base(self, id: str) -> AgentBaseTable:
        return AgentBaseTable(
            **self.mysql_client.select_by_id(
                table_name=AgentBaseTable.__tablename__, id=id
            )
        )

    def _get_agent_node(self, id: str) -> AgentNodeTable:
        return AgentNodeTable(
            **self.mysql_client.select_by_id(
                table_name=AgentNodeTable.__tablename__, id=id
            )
        )

    def get_graph(self, id: str) -> CompiledStateGraph:
        builder = StateGraph(GraphState)

        for node in self._get_nodes(graph_id=id):
            if node.type == "agent":
                agent_node = self._get_agent_node(id=node.agentNodeId)
                agent_base = self._get_agent_base(id=agent_node.agentBaseId)
                agent = self.agent_base_name_class_map[agent_base.name](
                    model=agent_node.customModel,
                    system_prompt=agent_node.customPrompt,
                )
                builder.add_node(
                    node.id, self.node_type_step_func_map[agent_base.name](agent)
                )
            else:
                builder.add_node(node.id, self.node_type_step_func_map[node.type]())

            if node.isBaseEntryPoint:
                builder.set_entry_point(node.id)

        for edge in self._get_edges(graph_id=id):
            builder.add_edge(edge.fromNodeId, edge.toNodeId)

        graph = builder.compile()
        return graph
