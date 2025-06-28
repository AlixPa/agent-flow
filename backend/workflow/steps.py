from typing import cast

from _agents import ConversationalAgent
from _logger import get_logger
from pydantic_ai import messages

from .graph_state import GraphState

logger = get_logger()


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
