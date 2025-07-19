from datetime import datetime

from fastapi import APIRouter
from src.config.formats import DateTimeFormat
from src.logger import get_logger

router = APIRouter(prefix="/health")
logger = get_logger()


@router.get("")
async def health_checkpoint():
    logger.info(f"Got asked for a health check.")
    return {
        "status": "ok",
        "timestamp": datetime.now().strftime(DateTimeFormat.ISO_8601_UTC),
    }
