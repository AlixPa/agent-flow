from typing import Any, Callable, Coroutine, Type

from src.agents.base import BaseAgent
from src.agents.step_agents import ConversationalAgent, ConversationalAgentConfig

from .graph_state import GraphState
from .steps import get_step_conversational_agent, get_step_input, get_step_output


class BuilderConfig:
    map_name_agent: dict[str, Type[BaseAgent]] = {
        ConversationalAgentConfig.AGENT_BASE_NAME: ConversationalAgent,
    }

    map_name_step_no_agent: dict[
        str,
        Callable[[], Callable[[GraphState], Coroutine[Any, Any, GraphState]]],
    ] = {
        "input": get_step_input,
        "output": get_step_output,
    }

    map_name_step_with_agent: dict[
        str,
        Callable[
            [BaseAgent],
            Callable[[GraphState], Coroutine[Any, Any, GraphState]],
        ],
    ] = {
        ConversationalAgentConfig.AGENT_BASE_NAME: get_step_conversational_agent,
    }
