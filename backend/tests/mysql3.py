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
    users = client.select(table=UserTable)
    logger.info(users)
    logger.info([u.to_dict() for u in users])
