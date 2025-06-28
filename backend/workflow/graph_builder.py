from _agents import ConversationalAgent
from _clients import MysqlClient
from _logger import get_logger
from _models import AgentBaseTable, AgentNodeTable, EdgeTable, NodeTable
from langgraph.graph import StateGraph
from langgraph.graph.state import CompiledStateGraph

from .graph_state import GraphState
from .steps import get_step_conversational_agent, get_step_input, get_step_output

logger = get_logger()


class GraphBuilder:
    def __init__(self) -> None:
        self.mysql_client = MysqlClient()
        self.agent_base_name_class_map = {"conversational_agent": ConversationalAgent}
        self.agent_base_name_step_map = {
            "conversational_agent": get_step_conversational_agent
        }

    def _get_nodes(self, graph_id: str) -> list[NodeTable]:
        return [
            NodeTable(**node)
            for node in self.mysql_client.select(
                table_name=NodeTable.__tablename__,
                cond_eq={"graphId": graph_id},
            )
        ]

    def _get_edges(self, graph_id: str) -> list[EdgeTable]:
        return [
            EdgeTable(**edge)
            for edge in self.mysql_client.select(
                table_name=EdgeTable.__tablename__,
                cond_eq={"graphId": graph_id},
            )
        ]

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
            if node.type == "input":
                builder.add_node(node.id, get_step_input())
            elif node.type == "output":
                builder.add_node(node.id, get_step_output())
            elif node.type == "agent":
                agent_node = self._get_agent_node(id=node.agentNodeId)
                agent_base = self._get_agent_base(id=agent_node.agentBaseId)
                if agent_node.prompt:
                    agent = self.agent_base_name_class_map[agent_base.name](
                        system_prompt=agent_node.prompt
                    )
                else:
                    agent = self.agent_base_name_class_map[agent_base.name]()
                builder.add_node(
                    node.id, self.agent_base_name_step_map[agent_base.name](agent)
                )

            if node.isBaseEntryPoint:
                builder.set_entry_point(node.id)

        for edge in self._get_edges(graph_id=id):
            builder.add_edge(edge.fromNodeId, edge.toNodeId)

        graph = builder.compile()
        return graph
