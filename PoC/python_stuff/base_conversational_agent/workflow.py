from typing import TypedDict

from langgraph.graph import StateGraph

from .agents import agent_conversation


class GraphState(TypedDict):
    user: str
    agent: str


def step_input(state: GraphState) -> GraphState:
    return {**state, "user": input("\nEnter any task:")}


def step_output(state: GraphState) -> GraphState:
    print(f"Response: {state['agent']}")
    return state


async def step_agent_conversation(state: GraphState) -> GraphState:
    result = await agent_conversation.run(user_prompt=state["user"])
    return {**state, "agent": result.output}


builder = StateGraph(GraphState)

builder.add_node("ConversationAgent", step_agent_conversation)
builder.add_node("InputTime", step_input)
builder.add_node("OutputTime", step_output)

builder.set_entry_point("InputTime")

builder.add_edge("InputTime", "ConversationAgent")
builder.add_edge("ConversationAgent", "OutputTime")
builder.add_edge("OutputTime", "InputTime")

graph = builder.compile()
