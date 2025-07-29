from src.config.llms import LLMsNames


class BaseAgentConfig:
    AGENT_BASE_NAME: str = "base_agent"
    MODEL: str = LLMsNames.gpt_4_1_mini
    SYSTEM_PROMPT: str = "Your are an agent."
