from asgi_correlation_id.middleware import CorrelationIdMiddleware, is_valid_uuid4
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api import api_router
from src.clients.mysql import MysqlClientWriter
from src.config.default_db_settings import DefaultDbSettings
from src.config.env_var import ENV
from src.config.runtime import ServiceEnv
from src.models.database import ConversationTable, GraphTable, NodeTable, UserTable

## Init db with default values
mysql_client = MysqlClientWriter()
mysql_client.start_transaction()
try:
    mysql_client.insert_one(
        table=UserTable,
        to_insert=DefaultDbSettings.USER,
        or_ignore=True,
    )

    mysql_client.insert_one(
        table=GraphTable,
        to_insert=DefaultDbSettings.GRAPH,
        or_ignore=True,
    )

    mysql_client.insert_one(
        table=ConversationTable,
        to_insert=DefaultDbSettings.CONVERSATION,
        or_ignore=True,
    )

    mysql_client.insert_one(
        table=NodeTable,
        to_insert=DefaultDbSettings.NODE,
        or_ignore=True,
    )
except Exception:
    mysql_client.rollback()
    raise
else:
    mysql_client.commit()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

app.add_middleware(
    CorrelationIdMiddleware,
    header_name="X-Correlation-ID",
    update_request_header=True,
    validator=None if ENV == ServiceEnv.LOCAL else is_valid_uuid4,
)
