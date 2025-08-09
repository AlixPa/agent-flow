from pydantic import BaseModel


class ConversationIdsResponse(BaseModel):
    request_graph_id: str
    conversation_ids: list[str]
