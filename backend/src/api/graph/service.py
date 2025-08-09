from src.clients.mysql import AMysqlClientReader
from src.exceptions.http import WrongArgumentException
from src.logger import get_logger
from src.models.database import ConversationTable, GraphTable

logger = get_logger()


async def load_conversations(graph_id: str) -> list[str]:
    mysql_reader = AMysqlClientReader(logger)
    if not await mysql_reader.id_exists(table=GraphTable, id=graph_id):
        raise WrongArgumentException(f"no graph found with the {graph_id=} provided")

    conversations = await mysql_reader.select(
        table=ConversationTable.__tablename__,
        select_col=["id"],
        cond_equal=dict(graphId=graph_id),
    )
    return [str(c["id"]) for c in conversations]
