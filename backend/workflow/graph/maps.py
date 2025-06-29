from typing import Callable, Type, TypedDict

from _agents import ConversationalAgent

from .steps import get_step_conversational_agent, get_step_input, get_step_output


class AgentBaseNameClassMap(TypedDict):
    conversational_agent: Type[ConversationalAgent]


agent_base_name_class_map: AgentBaseNameClassMap = {
    "conversational_agent": ConversationalAgent
}


class NodeTypeStepFuncMap(TypedDict):
    input: Type[Callable]
    output: Type[Callable]
    conversational_agent: Type[Callable]


node_type_step_func_map: NodeTypeStepFuncMap = {
    "input": get_step_input,
    "output": get_step_output,
    "conversational_agent": get_step_conversational_agent,
}
