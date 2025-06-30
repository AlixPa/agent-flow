import sys
from pathlib import Path

import logfire
from asgi_correlation_id.middleware import CorrelationIdMiddleware, is_valid_uuid4
from fastapi import FastAPI

root_path = Path(__file__).resolve().parent
sys.path.append(str(root_path))

from _config import ENV, ServiceEnv
from api import health_router

logfire.configure()
logfire.instrument_pydantic_ai()

app = FastAPI()

app.include_router(health_router)
app.add_middleware(
    CorrelationIdMiddleware,
    header_name="X-Correlation-ID",
    update_request_header=True,
    validator=None if ENV == ServiceEnv.LOCAL else is_valid_uuid4,
)
