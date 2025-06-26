from _config import ConversationalAgentConfig

from .base import BaseAgent


class ConversationalAgent(BaseAgent):
    def __init__(
        self,
        model: str = ConversationalAgentConfig.MODEL,
        system_prompt: str = ConversationalAgentConfig.SYSTEM_PROMPT,
        instrument: bool = True,
    ) -> None:
        super().__init__(
            model=model,
            system_prompt=system_prompt,
            instrument=instrument,
        )
