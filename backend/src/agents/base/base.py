from abc import ABC
from logging import Logger
from typing import Any, Type

from pydantic import BaseModel
from pydantic_ai import Agent, agent, messages, models, settings, usage
from src.clients.mysql import AMysqlClientWriter
from src.config.llms import CostPerInputToken, CostPerOutputToken
from src.logger import get_logger
from src.models.database import ExpenseTable
from src.workflow.graph.state import GraphState

from .config import BaseAgentConfig

base_logger = get_logger()


class BaseAgent(ABC):
    def __init__(
        self,
        model: str | None = None,
        system_prompt: str | None = None,
        name: str | None = None,
        instrument: bool = True,
        logger: Logger | None = None,
    ) -> None:
        self.model = model or BaseAgentConfig.MODEL
        self.name = name or BaseAgentConfig.AGENT_BASE_NAME
        self.agent = Agent(
            instrument=instrument,
            model=model or BaseAgentConfig.MODEL,
            system_prompt=system_prompt or BaseAgentConfig.SYSTEM_PROMPT,
        )
        self.logger = logger or base_logger
        self.amysql_writter = AMysqlClientWriter(logger=self.logger)

    async def run(
        self,
        user_prompt: str,
        state: GraphState,
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
        self.logger.debug(f"Called {self.__class__=} with {user_prompt=}. {state=}")

        response = await self.agent.run(
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

        request_tokens = response.usage().request_tokens or 0
        response_tokens = response.usage().response_tokens or 0

        cost = 0.0
        cost += float(request_tokens) * CostPerInputToken[self.model]
        cost += float(response_tokens) * CostPerOutputToken[self.model]

        if cost:
            expense = ExpenseTable(
                cost=cost,
                source=self.name,
                graphId=state.graph.id,
                nodeId=state.entry_node.id,
                conversationId=state.conversation.id,
                userId=state.user.id,
            )

            self.logger.info(expense)
            await self.amysql_writter.insert_one(table=ExpenseTable, to_insert=expense)

        return response
