from pydantic import BaseModel


class ConversationRequest(BaseModel):
    conversation_id: str
    graph_id: str
    ## TODO: user_id should eventually not be None
    user_id: str | None = None
    state_id: str | None = None
    user_message: str | None = None


class ConversationIdsResponse(BaseModel):
    request_graph_id: str
    conversation_ids: list[str]


class WrongArgumentException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
