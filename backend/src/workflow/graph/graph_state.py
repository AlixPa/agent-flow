from pydantic import BaseModel, Field
from pydantic_ai import messages


class GraphState(BaseModel):
    message_history: list[messages.ModelMessage] = Field(default=list())
    last_user_message: str = Field(default="")
    last_ai_message: str = Field(default="")

    graph_id: str | None = Field(default=None)
    conversation_id: str | None = Field(default=None)
    entry_node_id: str | None = Field(default=None)
    user_id: str | None = Field(default=None)
