from logging import Logger
from typing import Type, TypeVar

from src.clients.mysql import AMysqlClientReader, AMySqlIdNotFoundError
from src.exceptions.http import HTTPWrongAttributesException
from src.models.database import BaseTableModel

GenericTableModel = TypeVar("GenericTableModel", bound=BaseTableModel)


async def load_row_from_db(
    table: Type[GenericTableModel], id: str, logger: Logger
) -> GenericTableModel:
    mysql_client = AMysqlClientReader(logger)
    try:
        row = await mysql_client.select_by_id(table=table, id=id)
    except AMySqlIdNotFoundError:
        logger.error(
            f"Failed to load {table.__tablename__} in load_row_from_db, {id=} is not existing."
        )
        raise HTTPWrongAttributesException(
            f"no {table.__tablename__} founded with the {table.__tablename__}_id provided."
        )
    return row
