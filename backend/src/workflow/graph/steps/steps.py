from src.agents.base import BaseAgent
from src.agents.step_agents import ConversationalAgent
from src.clients.messenger import StreamMessage
from src.models.database import NodeTable
from src.workflow.graph.state import GraphState


def get_step_input(self_node: NodeTable):
    async def step_input(state: GraphState) -> GraphState:
        if state.skip_next_input:
            state.skip_next_input = False
        else:
            await state.messenger.send(
                StreamMessage(
                    current_node_id=self_node.id,
                )
            )
            state.stop_execution = True
        return state

    return step_input


def get_step_output(self_node: NodeTable):
    async def step_output(state: GraphState) -> GraphState:
        message_text = (
            state.message_history.messages[-1].text
            if state.message_history.messages
            else ""
        )
        await state.messenger.send(
            StreamMessage(
                text=message_text,
                current_node_id=self_node.id,
            )
        )
        return state

    return step_output


def get_step_conversational_agent(agent: BaseAgent, self_node: NodeTable):
    assert isinstance(agent, ConversationalAgent), "Expected ConversationalAgent"

    async def step_agent_conversation(state: GraphState) -> GraphState:
        await state.messenger.send(
            StreamMessage(
                current_node_id=self_node.id,
            )
        )
        next_message = await agent.generate_next_message(
            messages=state.message_history.messages,
            state=state,
        )
        state.message_history.messages.append(next_message)
        return state

    return step_agent_conversation
