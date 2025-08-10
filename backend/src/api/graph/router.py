from fastapi import APIRouter
from src.exceptions.http import HTTPWrongAttributesException, WrongArgumentException
from src.logger import get_logger

from .models import ConversationIdsResponse
from .service import load_conversations

router = APIRouter(prefix="/graph")
logger = get_logger()


@router.get("/{graph_id}/conversations", response_model=ConversationIdsResponse)
async def get_conversations_for_graph(graph_id: str) -> ConversationIdsResponse:
    try:
        logger.info(f"On GET /graph/{{graph_id}}/conversations got {graph_id=}")
        conversations_ids = await load_conversations(graph_id)
    except WrongArgumentException as e:
        raise HTTPWrongAttributesException(str(e))

    return ConversationIdsResponse(
        request_graph_id=graph_id, conversation_ids=conversations_ids
    )
