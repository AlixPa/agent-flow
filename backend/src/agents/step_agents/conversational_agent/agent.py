from collections.abc import Sequence
from typing import Any, Type

from pydantic import BaseModel
from pydantic_ai import agent, messages, models, settings, usage
from src.agents.base import BaseAgent
from src.workflow.graph.graph_state import GraphState, Message

from .config import ConversationalAgentConfig


class ConversationalAgent(BaseAgent):
    def __init__(
        self,
        model: str = ConversationalAgentConfig.MODEL,
        system_prompt: str = ConversationalAgentConfig.SYSTEM_PROMPT,
        instrument: bool = True,
        name: str = ConversationalAgentConfig.AGENT_BASE_NAME,
    ) -> None:
        super().__init__(
            model=model,
            system_prompt=system_prompt,
            instrument=instrument,
            name=name,
        )

    async def generate_next_message(
        self,
        messages: list[Message],
        state: GraphState,
    ) -> Message:
        user_prompt = "\n".join([str(m) for m in messages])
        result = await super().run(user_prompt=user_prompt, state=state)
        return Message(speaker=self.name, text=str(result.output))
