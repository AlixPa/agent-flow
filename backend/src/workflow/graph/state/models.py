from pydantic import BaseModel, Field
from src.clients.messenger import Messenger
from src.config.default_db_settings import DefaultDbSettings
from src.models.database import (
    ConversationTable,
    GraphStateTable,
    GraphTable,
    NodeTable,
    UserTable,
)


class ConversationMessage(BaseModel):
    def __str__(self) -> str:
        return f"**{self.speaker}**: {self.text}"

    speaker: str = Field(default="")
    text: str = Field(default="")


class MessageHistory(BaseModel):
    messages: list[ConversationMessage] = Field(default=list())


class GraphState(BaseModel):
    message_history: MessageHistory = Field(default=MessageHistory())

    messenger: Messenger = Field(
        description="Messenger used to communicate with frontend."
    )
    skip_next_input: bool = Field(
        description="To handle the user input, once we receive it we should skip the input step to not loop forever.",
        default=False,
    )
    stop_execution: bool = Field(
        description="If set to True, then the step by step graph exec should stop.",
        default=False,
    )

    conversation: ConversationTable = Field()
    entry_node: NodeTable = Field(default=DefaultDbSettings.NODE)
    graph: GraphTable = Field()
    user: UserTable = Field(default=DefaultDbSettings.USER)

    model_config = {"arbitrary_types_allowed": True}
