import sys
from pathlib import Path

ROOT_PATH = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_PATH))

from _clients import MysqlClient
from _config import ENV, ServiceEnv
from _logger import get_logger
from _models import GraphTable, NodeTable, UserTable

logger = get_logger()

if __name__ == "__main__":
    if ENV != ServiceEnv.LOCAL:
        raise Exception("Should run this particular unit test locally")

    client = MysqlClient()

    user_test = UserTable()
    logger.info(f"Will insert {user_test.to_dict()}")
    logger.info(f"Before: {client.select(table_name=UserTable.__tablename__)}")
    client.insert_one(
        table_name=UserTable.__tablename__, object_to_insert=user_test.to_dict()
    )
    logger.info(f"After: {client.select(table_name=UserTable.__tablename__)}")

    graph_test = GraphTable(name="my_test_graph", userId=user_test.id)
    logger.info(f"Will insert {graph_test.to_dict()}")
    logger.info(f"Before: {client.select(table_name=GraphTable.__tablename__)}")
    client.insert_one(
        table_name=GraphTable.__tablename__, object_to_insert=graph_test.to_dict()
    )
    logger.info(f"After: {client.select(table_name=GraphTable.__tablename__)}")

    graph_test.name = "new_name"
    logger.info(f"Will update {graph_test.to_dict()}")
    logger.info(
        f"Before: {client.select_by_id(table_name=GraphTable.__tablename__, id=graph_test.id)}"
    )
    client.update_by_id(
        table_name=GraphTable.__tablename__,
        update_col_value=graph_test.to_dict(include_col=["name"]),
        id=graph_test.id,
    )
    logger.info(
        f"After: {client.select_by_id(table_name=GraphTable.__tablename__, id=graph_test.id)}"
    )

    logger.info(f"Will delete {graph_test.to_dict()}")
    logger.info(f"Before: {client.select(table_name=GraphTable.__tablename__)}")
    client.delete_by_id(
        table_name=GraphTable.__tablename__,
        id=graph_test.id,
    )
    logger.info(f"After: {client.select(table_name=GraphTable.__tablename__)}")
