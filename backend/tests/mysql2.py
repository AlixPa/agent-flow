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

    users_test = [UserTable() for _ in range(5)]
    logger.info(f"Will insert {[u.to_dict() for u in users_test]}")
    logger.info(f"Before: {client.select(table_name=UserTable.__tablename__)}")
    client.insert(
        table_name=UserTable.__tablename__, to_insert=[u.to_dict() for u in users_test]
    )
    logger.info(f"After: {client.select(table_name=UserTable.__tablename__)}")

    graphs_test = [
        GraphTable(userId=users_test[i].id, name=f"test_graph{i}")
        for i in range(len(users_test))
    ]
    logger.info(f"Will insert {[g.to_dict() for g in graphs_test]}")
    logger.info(f"Before: {client.select(table_name=GraphTable.__tablename__)}")
    client.insert(
        table_name=GraphTable.__tablename__,
        to_insert=[g.to_dict() for g in graphs_test],
    )
    logger.info(f"After: {client.select(table_name=GraphTable.__tablename__)}")

    logger.info(f"Will update graphs with 'new_name' (except id 'graph1')")
    logger.info(f"Before: {client.select(table_name=GraphTable.__tablename__)}")
    client.update(
        table_name=GraphTable.__tablename__,
        update_col_value=dict(name="new_name"),
        cond_non_equal=dict(id="graph1"),
    )
    logger.info(f"After: {client.select(table_name=GraphTable.__tablename__)}")
