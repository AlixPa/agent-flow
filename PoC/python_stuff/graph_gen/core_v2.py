from typing import cast

from _agents import ConversationalAgent
from _clients import MysqlClient
from _logger import get_logger
from _models import AgentBaseTable, AgentNodeTable, EdgeTable, NodeTable
from langgraph.graph import StateGraph
from langgraph.graph.state import CompiledStateGraph
from pydantic import BaseModel, Field
from pydantic_ai import messages

logger = get_logger("graphBuilder_logger")


class GraphState(BaseModel):
    message_history: list[messages.ModelMessage] = Field(default=list())
    last_user_message: str = Field(default="")
    last_ai_message: str = Field(default="")


def get_step_input():
    def step_input(state: GraphState) -> GraphState:
        state.last_user_message = input("\nEnter any task:")
        return state

    return step_input


def get_step_output():
    def step_output(state: GraphState) -> GraphState:
        print(f"Response: {state.last_ai_message}")
        return state

    return step_output


def get_step_conversational_agent(agent: ConversationalAgent):
    async def step_agent_conversation(state: GraphState) -> GraphState:
        result = await agent.run(
            user_prompt=state.last_user_message, message_history=state.message_history
        )
        new_messages = result.new_messages()
        message_user = cast(messages.TextPart, new_messages[-2].parts[-1])
        message_user.content = "**Bob**: " + message_user.content
        message_llm = cast(messages.TextPart, new_messages[-1].parts[-1])
        message_llm.content = "**Assistant**: " + message_llm.content
        for mes in new_messages:
            logger.info(mes)
        state.message_history.extend(new_messages)
        state.last_ai_message = result.output
        return state

    return step_agent_conversation


class GraphBuilder:
    def __init__(self) -> None:
        self.mysql_client = MysqlClient(logger)
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
