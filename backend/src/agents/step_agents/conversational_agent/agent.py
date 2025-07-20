from src.agents.base import BaseAgent

from .config import ConversationalAgentConfig


class ConversationalAgent(BaseAgent):
    def __init__(
        self,
        model: str | None = None,
        system_prompt: str | None = None,
        instrument: bool = True,
        name: str | None = None,
    ) -> None:
        super().__init__(
            model=model or ConversationalAgentConfig.MODEL,
            system_prompt=system_prompt or ConversationalAgentConfig.SYSTEM_PROMPT,
            instrument=instrument,
            name=ConversationalAgentConfig.AGENT_BASE_NAME,
        )
