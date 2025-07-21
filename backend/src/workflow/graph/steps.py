from src.agents.base import BaseAgent
from src.agents.step_agents import ConversationalAgent

from .graph_state import GraphState, Message


## TODO: Of course this should be coming from frontend, temporary input()
def get_step_input():
    async def step_input(state: GraphState) -> GraphState:
        new_message = Message(speaker=state.user.name, text=input("\nEnter any task:"))
        state.message_history.append(new_message)
        return state

    return step_input


## TODO: Of course this should be sent from frontend, temporary output()
def get_step_output():
    async def step_output(state: GraphState) -> GraphState:
        message_text = state.message_history[-1].text if state.message_history else ""
        print(f"Response: {message_text}")
        return state

    return step_output


def get_step_conversational_agent(agent: BaseAgent):
    assert isinstance(agent, ConversationalAgent), "Expected ConversationalAgent"

    async def step_agent_conversation(state: GraphState) -> GraphState:
        next_message = await agent.generate_next_message(
            messages=state.message_history,
            state=state,
        )
        state.message_history.append(next_message)
        return state

    return step_agent_conversation
