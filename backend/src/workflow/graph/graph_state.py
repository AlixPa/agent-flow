from pydantic import BaseModel, Field
from src.config.default_db_settings import DefaultDbSettings
from src.models.database import ConversationTable, GraphTable, NodeTable, UserTable


class Message(BaseModel):
    def __str__(self) -> str:
        return f"**{self.speaker}**: {self.text}"

    speaker: str = Field(default="")
    text: str = Field(default="")


class GraphState(BaseModel):
    message_history: list[Message] = Field(default=list())

    graph: GraphTable = Field(default=DefaultDbSettings.GRAPH)
    conversation: ConversationTable = Field(default=DefaultDbSettings.CONVERSATION)
    entry_node: NodeTable = Field(default=DefaultDbSettings.NODE)
    user: UserTable = Field(default=DefaultDbSettings.USER)
