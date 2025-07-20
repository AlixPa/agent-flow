from pathlib import Path

import logfire
from dotenv import load_dotenv

REPO_ROOT_PATH = Path(__file__).resolve().parents[2]
load_dotenv(
    dotenv_path=REPO_ROOT_PATH / ".env",
    override=False,
)
logfire.configure()
logfire.instrument_pydantic_ai()

from src.clients import MysqlClientWriter
from src.config.default_db_settings import DefaultDbSettings
from src.models.database import ConversationTable, GraphTable, NodeTable, UserTable

mysql_client = MysqlClientWriter()
mysql_client.start_transaction()
try:
    user = UserTable(id=DefaultDbSettings.DEFAULT_ID)
    mysql_client.insert_one(
        table=UserTable,
        to_insert=user.to_dict(),
        or_ignore=True,
    )

    graph = GraphTable(
        name=DefaultDbSettings.DEFAULT_NAME,
        userId=user.id,
        id=DefaultDbSettings.DEFAULT_ID,
    )
    mysql_client.insert_one(
        table=GraphTable,
        to_insert=graph.to_dict(),
        or_ignore=True,
    )

    conversation = ConversationTable(
        graphId=graph.id,
        userId=user.id,
        id=DefaultDbSettings.DEFAULT_ID,
    )
    mysql_client.insert_one(
        table=ConversationTable,
        to_insert=conversation.to_dict(),
        or_ignore=True,
    )

    node = NodeTable(
        type=DefaultDbSettings.DEFAULT_NAME,
        graphId=graph.id,
        id=DefaultDbSettings.DEFAULT_ID,
    )
    mysql_client.insert_one(
        table=NodeTable,
        to_insert=node.to_dict(),
        or_ignore=True,
    )
except Exception:
    mysql_client.rollback()
else:
    mysql_client.commit()
