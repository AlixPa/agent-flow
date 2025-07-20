from abc import ABC
from collections.abc import Sequence
from logging import Logger
from typing import Any, Type

from pydantic import BaseModel
from pydantic_ai import Agent, agent, messages, models, settings, usage
from src.clients import AMysqlClientWriter
from src.logger import get_logger
from src.models.database import expense

logger = get_logger()


class BaseAgent(ABC):
    def __init__(
        self,
        model: str,
        system_prompt: str,
        instrument: bool = True,
        logger: Logger = logger,
        silent: bool = False,
    ) -> None:
        self.agent = Agent(
            instrument=instrument,
            model=model,
            system_prompt=system_prompt,
        )
        self.logger = logger
        self.silent = silent

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
        if not self.silent:
            self.logger.debug(f"Called {self.__class__=} with {user_prompt=}")
        ## TODO: Add config.default_db_settings with stuff like "default_user", "default_conversation", ...
        ## TODO: Add in the src/__init__.py the init of db writting inside the db all the default stuff
        ## TODO: Get the expense out of it, and record in the db. If not in state, then use default
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
