class LLMsNames:
    gpt_4_1 = "openai:gpt-4.1"
    gpt_4_1_mini = "openai:gpt-4.1-mini"
    gpt_4_1_nano = "openai:gpt-4.1-nano"
    gpt_o3 = "openai:o3"

    claude_4 = "anthropic:claude-sonnet-4-0"
    claude_3_7 = "anthropic:claude-3-7-sonnet-latest"
    claude_3_5_haiku = "anthropic:claude-3-5-haiku-latest"


CostPerInputToken = {
    "openai:gpt-4.1": 2.0 * (1.0 / 10**6),
    "openai:gpt-4.1-mini": 0.4 * (1.0 / 10**6),
    "openai:gpt-4.1-nano": 0.1 * (1.0 / 10**6),
    "openai:o3": 2.0 * (1.0 / 10**6),
    "anthropic:claude-sonnet-4-0": 3.0 * (1.0 / 10**6),
    "anthropic:claude-3-7-sonnet-latest": 3.0 * (1.0 / 10**6),
    "anthropic:claude-3-5-haiku-latest": 0.8 * (1.0 / 10**6),
}

CostPerOutputToken = {
    "openai:gpt-4.1": 8.0 * (1.0 / 10**6),
    "openai:gpt-4.1-mini": 1.6 * (1.0 / 10**6),
    "openai:gpt-4.1-nano": 0.4 * (1.0 / 10**6),
    "openai:o3": 8.0 * (1.0 / 10**6),
    "anthropic:claude-sonnet-4-0": 15.0 * (1.0 / 10**6),
    "anthropic:claude-3-7-sonnet-latest": 15.0 * (1.0 / 10**6),
    "anthropic:claude-3-5-haiku-latest": 4 * (1.0 / 10**6),
}
