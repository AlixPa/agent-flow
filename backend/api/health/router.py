from datetime import datetime

from _config import DateTimeFormat
from _logger import get_logger
from fastapi import APIRouter

router = APIRouter(prefix="/health")
logger = get_logger()


@router.get("")
async def health_checkpoint():
    logger.info(f"Got asked for a health check.")
    return {
        "status": "ok",
        "timestamp": datetime.now().strftime(DateTimeFormat.ISO_8601_UTC),
    }
