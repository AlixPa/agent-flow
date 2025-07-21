from pydantic import BaseModel, Field
from src.config.default_db_settings import DefaultDbSettings
from src.models.database import ConversationTable, GraphTable, NodeTable, UserTable


class Message(BaseModel):
    def __str__(self) -> str:
        return f"**{self.speaker}**: {self.text}"

    speaker: str = Field(default="")
    text: str = Field(default="")


class MessageHistory(BaseModel):
    messages: list[Message] = Field(default=list())


class GraphState(BaseModel):
    message_history: MessageHistory = Field(default=MessageHistory())

    conversation: ConversationTable = Field(default=DefaultDbSettings.CONVERSATION)
    entry_node: NodeTable = Field(default=DefaultDbSettings.NODE)
    graph: GraphTable = Field(default=DefaultDbSettings.GRAPH)
    user: UserTable = Field(default=DefaultDbSettings.USER)
