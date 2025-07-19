from asgi_correlation_id.middleware import CorrelationIdMiddleware, is_valid_uuid4
from fastapi import FastAPI
from src.api import health_router
from src.config.env_var import ENV
from src.config.runtime import ServiceEnv

app = FastAPI()

app.include_router(health_router)

app.add_middleware(
    CorrelationIdMiddleware,
    header_name="X-Correlation-ID",
    update_request_header=True,
    validator=None if ENV == ServiceEnv.LOCAL else is_valid_uuid4,
)
