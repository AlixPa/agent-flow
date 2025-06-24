from typing import TypedDict

from langgraph.graph import StateGraph

from .agents import agent_answer, agent_formulize


class GraphState(TypedDict):
    task: str
    question: str
    answer: str


def step_input(state: GraphState) -> GraphState:
    return {**state, "task": input("\nEnter any task:")}


def step_output(state: GraphState) -> GraphState:
    print(f"Response: {state['answer']}")
    return state


async def step_agent_formulize(state: GraphState) -> GraphState:
    result = await agent_formulize.run(user_prompt=state["task"])
    return {**state, "question": result.output}


async def step_agent_answer(state: GraphState) -> GraphState:
    result = await agent_answer.run(user_prompt=state["task"])
    return {**state, "answer": result.output}


builder = StateGraph(GraphState)

builder.add_node("FormulizeAgent", step_agent_formulize)
builder.add_node("AnswerAgent", step_agent_answer)
builder.add_node("InputTime", step_input)
builder.add_node("OutputTime", step_output)

builder.set_entry_point("InputTime")

builder.add_edge("InputTime", "FormulizeAgent")
builder.add_edge("FormulizeAgent", "AnswerAgent")
builder.add_edge("AnswerAgent", "OutputTime")
builder.add_edge("OutputTime", "InputTime")

graph = builder.compile()
