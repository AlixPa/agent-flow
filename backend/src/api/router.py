from fastapi import APIRouter

from .conversation import conversation_router
from .graph import graph_router
from .health import health_router

router = APIRouter(prefix="/api")

router.include_router(conversation_router)
router.include_router(graph_router)
router.include_router(health_router)
