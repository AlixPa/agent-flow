from abc import ABC
from collections.abc import Sequence
from typing import Any, Type

from pydantic import BaseModel
from pydantic_ai import Agent, agent, messages, models, settings, usage

from .config import ConversationalAgentConfig


class BaseAgent(ABC):
    def __init__(
        self,
        model: str,
        system_prompt: str,
        instrument: bool = True,
    ) -> None:
        self.agent = Agent(
            instrument=instrument,
            model=model,
            system_prompt=system_prompt,
        )

    async def run(
        self,
        user_prompt: str | Sequence[messages.UserContent] | None,
        *,
        output_type: Type[BaseModel] | None = None,
        message_history: list[messages.ModelMessage] | None = None,
        model: models.Model | models.KnownModelName | str | None = None,
        deps: Any = None,  # ...
        model_settings: settings.ModelSettings | None = None,
        usage_limits: usage.UsageLimits | None = None,
        usage: usage.Usage | None = None,
        infer_name: bool = True,
    ) -> agent.AgentRunResult[Any]:
        return await self.agent.run(
            user_prompt=user_prompt,
            output_type=output_type,
            message_history=message_history,
            model=model,
            deps=deps,
            model_settings=model_settings,
            usage_limits=usage_limits,
            usage=usage,
            infer_name=infer_name,
        )


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


agent_conversation = ConversationalAgent()
