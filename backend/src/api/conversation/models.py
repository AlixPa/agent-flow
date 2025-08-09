from pydantic import BaseModel
from src.workflow.graph.state import MessageHistory


class ConversationStreamRequest(BaseModel):
    conversation_id: str
    graph_id: str
    ## TODO: user_id should eventually not be None
    user_id: str | None = None
    state_id: str | None = None
    user_message: str | None = None


class Conversation(BaseModel):
    messages: MessageHistory
    node_id: str | None
    state_id: str


class ConversationResponse(BaseModel):
    request_conversation_id: str
    conversation: Conversation
