from src.agents.base import BaseAgent
from src.workflow.graph.state import GraphState, Message

from .config import ConversationalAgentConfig


class ConversationalAgent(BaseAgent):
    def __init__(
        self,
        model: str | None = None,
        system_prompt: str | None = None,
        name: str | None = None,
    ) -> None:
        super().__init__(
            model=model or ConversationalAgentConfig.MODEL,
            system_prompt=system_prompt or ConversationalAgentConfig.SYSTEM_PROMPT,
            name=name or ConversationalAgentConfig.AGENT_BASE_NAME,
        )

    async def generate_next_message(
        self,
        messages: list[Message],
        state: GraphState,
    ) -> Message:
        user_prompt = "\n".join([str(m) for m in messages])
        result = await super().run(user_prompt=user_prompt, state=state)
        return Message(speaker=self.name, text=str(result.output))
