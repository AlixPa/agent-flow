from datetime import datetime

from _utils import DateTimeFormat
from fastapi import APIRouter

router = APIRouter(prefix="/health")


@router.get("")
async def health_checkpoint():
    return {
        "status": "ok",
        "timestamp": datetime.now().strftime(DateTimeFormat.ISO_8601_UTC),
    }
