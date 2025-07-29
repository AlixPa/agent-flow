from logging import Logger

from src.agents.base import BaseAgent
from src.logger import get_logger
from src.workflow.graph.state import ConversationMessage, GraphState

from .config import ConversationalAgentConfig

base_logger = get_logger()


class ConversationalAgent(BaseAgent):
    def __init__(
        self,
        model: str | None = None,
        system_prompt: str | None = None,
        name: str | None = None,
        logger: Logger | None = None,
    ) -> None:
        super().__init__(
            model=model or ConversationalAgentConfig.MODEL,
            system_prompt=system_prompt or ConversationalAgentConfig.SYSTEM_PROMPT,
            name=name or ConversationalAgentConfig.AGENT_BASE_NAME,
            logger=logger or base_logger,
        )

    async def generate_next_message(
        self,
        messages: list[ConversationMessage],
        state: GraphState,
    ) -> ConversationMessage:
        user_prompt = "\n".join([str(m) for m in messages])
        result = await super().run(user_prompt=user_prompt, state=state)
        return ConversationMessage(speaker=self.name, text=str(result.output))
