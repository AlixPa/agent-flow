from _agents import ConversationalAgent
from _clients import MysqlClient
from _logger import get_logger
from _models import AgentBaseTable, AgentNodeTable, EdgeTable, NodeTable
from langgraph.graph import StateGraph
from pydantic import BaseModel, Field
from pydantic_ai import messages

base_logger = get_logger()
graph_id = "graph1"
user_id = "user1"


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
        state.message_history.extend(result.new_messages())
        state.last_ai_message = result.output
        return state

    return step_agent_conversation


agent_base_name_class_map = {"conversational_agent": ConversationalAgent}
agent_base_name_step_map = {"conversational_agent": get_step_conversational_agent}

mysql_client = MysqlClient(base_logger)

nodes = [
    NodeTable(**node)
    for node in mysql_client.select(
        table_name=NodeTable.__tablename__,
        cond_eq={"graphId": graph_id},
    )
]

edges = [
    EdgeTable(**edge)
    for edge in mysql_client.select(
        table_name=EdgeTable.__tablename__,
        cond_eq={"graphId": graph_id},
    )
]


def get_agent_base(id: str) -> AgentBaseTable:
    return AgentBaseTable(
        **mysql_client.select_by_id(table_name=AgentBaseTable.__tablename__, id=id)
    )


def get_agent_node(id: str) -> AgentNodeTable:
    return AgentNodeTable(
        **mysql_client.select_by_id(table_name=AgentNodeTable.__tablename__, id=id)
    )


builder = StateGraph(GraphState)

for node in nodes:
    if node.type == "input":
        builder.add_node(node.id, get_step_input())
    elif node.type == "output":
        builder.add_node(node.id, get_step_output())
    elif node.type == "agent":
        agent_node = get_agent_node(id=node.agentNodeId)
        agent_base = get_agent_base(id=agent_node.agentBaseId)
        if agent_node.prompt:
            agent = agent_base_name_class_map[agent_base.name](
                system_prompt=agent_node.prompt
            )
        else:
            agent = agent_base_name_class_map[agent_base.name]()
        builder.add_node(node.id, agent_base_name_step_map[agent_base.name](agent))

    if node.isBaseEntryPoint:
        builder.set_entry_point(node.id)

for edge in edges:
    builder.add_edge(edge.fromNodeId, edge.toNodeId)

graph = builder.compile()
