from pydantic import BaseModel, Field


class StreamMessage(BaseModel):
    is_final_message: bool = Field(
        description="Always at false in the steps, True is only allowed by router.",
        default=False,
    )
    conversation_id: str = Field()
    text: str | None = Field(default=None)
    state_id: str | None = Field(default=None)
    current_node_id: str | None = Field(default=None)
