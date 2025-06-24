from pydantic_ai import Agent

agent_formulize = Agent(
    model="openai:gpt-4.1-mini",
    system_prompt="You are a smart agent. You will be given a task and need to formulate the task into a understable question.",
    instrument=True,
)

agent_answer = Agent(
    model="openai:gpt-4.1-mini",
    system_prompt="You are a smart agent. You will be given a question and need to answer accurately and concisely to the question.",
    instrument=True,
)
