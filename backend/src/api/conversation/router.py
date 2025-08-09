from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from src.config.default_db_settings import DefaultDbSettings
from src.exceptions.http import HTTPWrongAttributesException, WrongArgumentException
from src.logger import get_logger

from .models import ConversationRequest
from .service import get_stream_flow, start_state_existing_conv, start_state_new_conv

router = APIRouter(prefix="/conversation")
logger = get_logger()


@router.post("/stream", response_model=str)
async def stream_conversation(req: ConversationRequest) -> StreamingResponse:
    try:
        logger.info(f"On POST /conversation/stream_conversation got {req=}")

        # TODO: Implement real user id
        if req.user_id is None:
            req.user_id = DefaultDbSettings.USER.id

        if req.state_id:
            # Continue an existing conversation, meaning a user message must be present
            if not req.user_message:
                raise HTTPWrongAttributesException(
                    "state_id found but not user_message."
                )
            start_state = await start_state_existing_conv(
                state_id=req.state_id,
                user_message=req.user_message,
            )
        else:
            # Init the conversation, meaning a user message cannot be present at start
            if req.user_message:
                raise HTTPWrongAttributesException(
                    "user_message found but not state_id."
                )
            start_state = await start_state_new_conv(
                user_id=req.user_id,
                graph_id=req.graph_id,
                conversation_id=req.conversation_id,
            )

        logger.info(f"On POST /conversation/stream_conversation loaded {start_state=}")

        stream_flow = await get_stream_flow(
            graph_id=req.graph_id, start_state=start_state
        )
    except WrongArgumentException as e:
        raise HTTPWrongAttributesException(str(e))

    return StreamingResponse(
        stream_flow,
        media_type="text/event-stream",
    )
