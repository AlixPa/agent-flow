## TODO: Migrate to other than pymysql to support async
import traceback
from logging import Logger

import pymysql.cursors
from _config import MYSQL_DATABASE, MYSQL_HOST, MYSQL_PASSWORD, MYSQL_PORT, MYSQL_USER
from _logger import get_logger

from .exceptions import (
    MySqlDuplicateColumnUpdateError,
    MySqlNoConnectionError,
    MySqlNoUpdateValuesError,
    MySqlNoValueInsertionError,
    MySqlWrongQueryError,
)

base_logger = get_logger()


class MysqlClient:
    def __init__(self, logger: Logger | None = None):
        self.logger = logger if logger else base_logger
        self.connection: pymysql.Connection[pymysql.cursors.DictCursor] | None = None
        self.port = MYSQL_PORT
        self.host = MYSQL_HOST
        self.user = MYSQL_USER
        self.password = MYSQL_PASSWORD
        self.database = MYSQL_DATABASE
        self.__connect()

    def __connect(self):
        self.connection = pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            passwd=self.password,
            database=self.database,
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,
        )

    def check_alive(self):
        try:
            try:
                check_alive_res = self.execute("select 1;")
            except:
                check_alive_res = None
            if not check_alive_res:
                self.__connect()
        except:
            self.logger.critical("ERROR: Lost connection to Database.")
            raise MySqlNoConnectionError()

    def logging(self, cursor):
        self.logger.debug(
            f"MysqlClient executed: {str(cursor._executed)} {cursor.rowcount=}"
        )

    def generate_cond(
        self,
        cond_null: list[str] = list(),
        cond_not_null: list[str] = list(),
        cond_in: dict[str, list] = dict(),
        cond_equal: dict[str, object] = dict(),
        cond_non_equal: dict[str, object] = dict(),
        cond_less_or_eq: dict[str, object] = dict(),
        cond_greater_or_eq: dict[str, object] = dict(),
        cond_less: dict[str, object] = dict(),
        cond_greater: dict[str, object] = dict(),
    ) -> tuple[str, tuple]:
        """
        Function that generates the condition as well as the args for any query

        Returns
        -------
        str
            The condition Starting with WHERE of the sql query
        tuple
            The args parameter to give to MysqlClient.execute
        """
        conds = ["WHERE 1 = 1"]
        args = list()

        for col in cond_null:
            conds.append(f"AND {col} IS NULL")

        for col in cond_not_null:
            conds.append(f"AND {col} IS NOT NULL")

        for col, ls_val in cond_in.items():
            if len(ls_val) == 0:
                continue
            conds.append(f"AND {col} IN (" + ",".join(["%s"] * len(ls_val)) + ")")
            args.extend(ls_val)

        for col, val in cond_equal.items():
            conds.append(f"AND {col} = %s")
            args.append(val)

        for col, val in cond_non_equal.items():
            conds.append(f"AND {col} <> %s")
            args.append(val)

        for col, val in cond_less_or_eq.items():
            conds.append(f"AND {col} <= %s")
            args.append(val)

        for col, val in cond_greater_or_eq.items():
            conds.append(f"AND {col} >= %s")
            args.append(val)

        for col, val in cond_less.items():
            conds.append(f"AND {col} < %s")
            args.append(val)

        for col, val in cond_greater.items():
            conds.append(f"AND {col} > %s")
            args.append(val)

        return " ".join(conds), tuple(args)

    def delete(
        self,
        table_name: str,
        cond_null: list[str] = list(),
        cond_not_null: list[str] = list(),
        cond_in: dict[str, list] = dict(),
        cond_equal: dict[str, object] = dict(),
        cond_non_equal: dict[str, object] = dict(),
        cond_less_or_eq: dict[str, object] = dict(),
        cond_greater_or_eq: dict[str, object] = dict(),
        cond_less: dict[str, object] = dict(),
        cond_greater: dict[str, object] = dict(),
        silent: bool = False,
    ) -> tuple[dict[str, object], ...]:
        """Delete rows from a database table based on conditions.

        Parameters
        ----------
        table_name : str
            Name of the table to delete from
        cond_null : list[str], optional
            Columns that must be NULL
        cond_not_null : list[str], optional
            Columns that must not be NULL
        cond_in : dict[str, list], optional
            Column values that must be in given list
        cond_eq : dict[str, object], optional
            Column values that must equal given value
        cond_neq : dict[str, object], optional
            Column values that must not equal given value
        cond_leq : dict[str, object], optional
            Column values that must be less than or equal to given value
        cond_geq : dict[str, object], optional
            Column values that must be greater than or equal to given value
        cond_l : dict[str, object], optional
            Column values that must be less than given value
        cond_g : dict[str, object], optional
            Column values that must be greater than given value
        silent : bool, optional
            If True, suppress logging of the query execution, by default False

        Returns
        -------
        tuple
            Tuple containing the deleted rows' data

        Raises
        ------
        NoConnectionError
            If no database connection exists
        MySqlWrongQueryError
            If query is wrong
        """
        res_mysql = self.select(
            table_name=table_name,
            cond_equal=cond_equal,
            cond_greater=cond_greater,
            cond_greater_or_eq=cond_greater_or_eq,
            cond_in=cond_in,
            cond_less=cond_less,
            cond_less_or_eq=cond_less_or_eq,
            cond_non_equal=cond_non_equal,
            cond_not_null=cond_not_null,
            cond_null=cond_null,
            silent=True,
        )

        ids_to_delete_ls = [str(dt["id"]) for dt in res_mysql]

        if not ids_to_delete_ls:
            self.logger.info("nothing to update")
            return tuple()

        query_parts = [f"DELETE FROM {table_name}"]
        query_parts.append(f"WHERE id IN ({", ".join(["%s"]*len(ids_to_delete_ls))})")
        query_parts.append(";")

        self.execute(
            query=" ".join(query_parts), args=tuple(ids_to_delete_ls), silent=silent
        )
        self.connection.commit()  # type: ignore
        return res_mysql

    def execute(
        self, query: str, args: tuple | dict | None = None, silent=False
    ) -> tuple[dict[str, object], ...]:
        """Execute a SQL query and return the results.

        Parameters
        ----------
        query : str
            SQL query to execute
        args : tuple | dict | None, optional
            Parameters to pass to the query, by default None
        silent : bool, optional
            If True, suppress logging of the query execution, by default False

        Returns
        -------
        tuple
            Results of the query execution

        Raises
        ------
        NoConnectionError
            If no database connection exists
        MySqlWrongQueryError
            If query is wrong
        """
        if not self.connection:
            self.logger.error("could not execute query, no connection to Database")
            raise MySqlNoConnectionError()
        with self.connection.cursor() as cursor:
            try:
                cursor.execute(query=query, args=args)
                res = cursor.fetchall()
            except pymysql.err.ProgrammingError as e:
                self.logger.warning(
                    f"error while executing query, {traceback.format_exc()}"
                )
                raise MySqlWrongQueryError(f"{type(e)=}, {str(e)=}")
            if not silent:
                self.logging(cursor)
        return res

    def count(
        self,
        table_name: str,
        select_col: list[str] = list(),
        cond_null: list[str] = list(),
        cond_not_null: list[str] = list(),
        cond_in: dict[str, list] = dict(),
        cond_equal: dict[str, object] = dict(),
        cond_non_equal: dict[str, object] = dict(),
        cond_less_or_eq: dict[str, object] = dict(),
        cond_greater_or_eq: dict[str, object] = dict(),
        cond_less: dict[str, object] = dict(),
        cond_greater: dict[str, object] = dict(),
        silent: bool = False,
    ) -> int | None:
        """Execute a SELECT COUNT(...) query with various conditions.

        Parameters
        ----------
        table_name : str
            Name of the table to query
        select_col : list[str], optional
            List of columns to include in the COUNT(...), by default all columns
        cond_null : list[str], optional
            Columns that must be NULL
        cond_not_null : list[str], optional
            Columns that must not be NULL
        cond_in : dict[str, list], optional
            Column values that must be in given list
        cond_eq : dict[str, object], optional
            Column values that must equal given value
        cond_neq : dict[str, object], optional
            Column values that must not equal given value
        cond_leq : dict[str, object], optional
            Column values that must be less than or equal to given value
        cond_geq : dict[str, object], optional
            Column values that must be greater than or equal to given value
        cond_l : dict[str, object], optional
            Column values that must be less than given value
        cond_g : dict[str, object], optional
            Column values that must be greater than given value
        silent : bool, optional
            If True, suppress logging of the query execution, by default False

        Returns
        -------
        int
            result of the count
        None
            if query went wrong

        Raises
        ------
        NoConnectionError
            If no database connection exists
        MySqlWrongQueryError
            If query is wrong
        """
        query_parts = [
            f"SELECT COUNT({', '.join(select_col) if select_col else '*'}) AS ct FROM {table_name}"
        ]
        cond, args = self.generate_cond(
            cond_equal=cond_equal,
            cond_greater=cond_greater,
            cond_greater_or_eq=cond_greater_or_eq,
            cond_in=cond_in,
            cond_less=cond_less,
            cond_less_or_eq=cond_less_or_eq,
            cond_non_equal=cond_non_equal,
            cond_not_null=cond_not_null,
            cond_null=cond_null,
        )

        query_parts.append(cond)
        query_parts.append(";")

        res_mysql = self.execute(query=" ".join(query_parts), args=args, silent=silent)
        if not res_mysql:
            return None
        res = res_mysql[0].get("ct", None)
        return int(str(res)) if res else None

    def select(
        self,
        table_name: str,
        select_col: list[str] = list(),
        cond_null: list[str] = list(),
        cond_not_null: list[str] = list(),
        cond_in: dict[str, list] = dict(),
        cond_equal: dict[str, object] = dict(),
        cond_non_equal: dict[str, object] = dict(),
        cond_less_or_eq: dict[str, object] = dict(),
        cond_greater_or_eq: dict[str, object] = dict(),
        cond_less: dict[str, object] = dict(),
        cond_greater: dict[str, object] = dict(),
        order_by: str = "",
        ascending_order: bool = True,
        limit: int = 0,
        offset: int = 0,
        silent: bool = False,
    ) -> tuple[dict[str, object], ...]:
        """Execute a SELECT query with various conditions.

        Parameters
        ----------
        table_name : str
            Name of the table to query
        select_col : list[str], optional
            List of columns to select, by default all columns
        cond_null : list[str], optional
            Columns that must be NULL
        cond_not_null : list[str], optional
            Columns that must not be NULL
        cond_in : dict[str, list], optional
            Column values that must be in given list
        cond_eq : dict[str, object], optional
            Column values that must equal given value
        cond_neq : dict[str, object], optional
            Column values that must not equal given value
        cond_leq : dict[str, object], optional
            Column values that must be less than or equal to given value
        cond_geq : dict[str, object], optional
            Column values that must be greater than or equal to given value
        cond_l : dict[str, object], optional
            Column values that must be less than given value
        cond_g : dict[str, object], optional
            Column values that must be greater than given value
        silent : bool, optional
            If True, suppress logging of the query execution, by default False
        limit : int | None, optional
            Maximum number of rows to return, 0 means alls, by default 0
        offset : int | None, optional
            Number of rows to skip before returning results, 0 means no offset, by default 0

        Returns
        -------
        tuple
            Query results as a tuple of dictionaries

        Raises
        ------
        NoConnectionError
            If no database connection exists
        MySqlWrongQueryError
            If query is wrong
        """
        query_parts = [
            f"SELECT {', '.join(select_col) if select_col else '*'} FROM {table_name}"
        ]
        cond, args = self.generate_cond(
            cond_equal=cond_equal,
            cond_greater=cond_greater,
            cond_greater_or_eq=cond_greater_or_eq,
            cond_in=cond_in,
            cond_less=cond_less,
            cond_less_or_eq=cond_less_or_eq,
            cond_non_equal=cond_non_equal,
            cond_not_null=cond_not_null,
            cond_null=cond_null,
        )
        query_parts.append(cond)
        if order_by:
            query_parts.append(
                f"ORDER BY {order_by} {'ASC' if ascending_order else 'DESC'}"
            )
        if limit > 0:
            query_parts.append(f"LIMIT {limit}")
            query_parts.append(f"OFFSET {offset}")
        query_parts.append(";")
        res_mysql = self.execute(query=" ".join(query_parts), args=args, silent=silent)
        return res_mysql

    def select_by_id(
        self,
        table_name: str,
        id: str,
        select_col: list[str] = list(),
        silent: bool = False,
    ) -> dict:
        """Select a row from a database table by its ID.

        Parameters
        ----------
        table_name : str
            Name of the table to select from
        id : str
            ID of the row to select
        select_col : list[str], optional
            List of columns to select, by default all columns
        silent : bool, optional
            If True, suppress logging of the query execution, by default False

        Returns
        -------
        dict
            Dictionary containing the row's data, empty dict if not found

        Raises
        ------
        NoConnectionError
            If no database connection exists
        MySqlWrongQueryError
            If query is wrong
        """
        res_mysql = self.select(
            table_name=table_name,
            select_col=select_col,
            cond_equal={"id": id},
            silent=silent,
        )
        if not res_mysql:
            return dict()
        return res_mysql[0]

    def delete_by_id(self, table_name: str, id: str, silent: bool = False) -> dict:
        """Delete a row from a database table by its ID.

        Parameters
        ----------
        table_name : str
            Name of the table to delete from
        id : str
            ID of the row to delete
        silent : bool, optional
            If True, suppress logging of the query execution, by default False

        Returns
        -------
        dict
            Dictionary containing the deleted row's data, empty dict if not found

        Raises
        ------
        NoConnectionError
            If no database connection exists
        MySqlWrongQueryError
            If query is wrong
        """
        res_mysql = self.delete(
            table_name=table_name, cond_equal={"id": id}, silent=silent
        )
        self.connection.commit()  # type: ignore
        return res_mysql[0] if res_mysql else dict()

    def close(self):
        if self.connection:
            self.connection.close()

    def insert_one(
        self,
        table_name: str,
        object_to_insert: dict[str, object],
        silent=False,
        or_ignore=False,
    ):
        """Insert a single row into a database table.

        Parameters
        ----------
        table_name : str
            Name of the table to insert into
        object_to_insert : dict
            Dictionary of column names and their corresponding values
        silent : bool, optional
            If True, suppress logging of the query execution, by default False
        or_ignore : bool, optional
            If True, use INSERT IGNORE, default False

        Raises
        ------
        NoValueInsertionError
            If values dictionary is empty
        NoConnectionError
            If no database connection exists
        MySqlWrongQueryError
            If query is wrong
        """
        if "createdAt" in object_to_insert:
            del object_to_insert["createdAt"]
        if "updatedAt" in object_to_insert:
            del object_to_insert["updatedAt"]

        if not object_to_insert:
            self.logger.warning("could not insert one, no object_to_insert given")
            raise MySqlNoValueInsertionError()

        query_parts = [f"INSERT {"IGNORE" if or_ignore else ""} INTO {table_name}"]
        query_parts.append(f"({", ".join([col for col in object_to_insert])})")
        query_parts.append(f"VALUES ({", ".join(["%s"] * len(object_to_insert))})")
        query_parts.append(";")

        self.execute(
            query=" ".join(query_parts),
            args=tuple(v for v in object_to_insert.values()),
            silent=silent,
        )
        self.connection.commit()  # type: ignore

    def update(
        self,
        table_name: str,
        update_col_col: dict[str, str] = dict(),
        update_col_value: dict[str, object] = dict(),
        cond_null: list[str] = list(),
        cond_not_null: list[str] = list(),
        cond_in: dict[str, list] = dict(),
        cond_equal: dict[str, object] = dict(),
        cond_non_equal: dict[str, object] = dict(),
        cond_less_or_eq: dict[str, object] = dict(),
        cond_greater_or_eq: dict[str, object] = dict(),
        cond_less: dict[str, object] = dict(),
        cond_greater: dict[str, object] = dict(),
        silent: bool = False,
    ) -> tuple[dict[str, object], ...]:
        """Update rows in a database table based on conditions.

        Parameters
        ----------
        table_name : str
            Name of the table to update
        update_col_col : dict[str, str], optional
            Dictionary mapping columns to update with other column values
        update_col_value : dict[str, object], optional
            Dictionary mapping columns to update with specific values
        cond_null : list[str], optional
            Columns that must be NULL
        cond_not_null : list[str], optional
            Columns that must not be NULL
        cond_in : dict[str, list], optional
            Column values that must be in given list
        cond_eq : dict[str, object], optional
            Column values that must equal given value
        cond_neq : dict[str, object], optional
            Column values that must not equal given value
        cond_leq : dict[str, object], optional
            Column values that must be less than or equal to given value
        cond_geq : dict[str, object], optional
            Column values that must be greater than or equal to given value
        cond_l : dict[str, object], optional
            Column values that must be less than given value
        cond_g : dict[str, object], optional
            Column values that must be greater than given value
        silent : bool, optional
            If True, suppress logging of the query execution, by default False

        Returns
        -------
        tuple
            Updated rows' data

        Raises
        ------
        NoConnectionError
            If no database connection exists
        DuplicateColumnUpdateError
            If a column appears in both update_col_col and update_col_value
        MySqlWrongQueryError
            If query is wrong
        """
        if "updatedAt" in update_col_col:
            del update_col_col["updatedAt"]
        if "updatedAt" in update_col_value:
            del update_col_value["updatedAt"]

        if not update_col_col and not update_col_value:
            raise MySqlNoUpdateValuesError()

        for col in update_col_col:
            if col in update_col_value:
                raise (MySqlDuplicateColumnUpdateError(column=col))
        for col in update_col_value:
            if col in update_col_col:
                raise (MySqlDuplicateColumnUpdateError(column=col))

        ids_to_update = self.select(
            table_name=table_name,
            select_col=["id"],
            cond_equal=cond_equal,
            cond_greater=cond_greater,
            cond_greater_or_eq=cond_greater_or_eq,
            cond_in=cond_in,
            cond_less=cond_less,
            cond_less_or_eq=cond_less_or_eq,
            cond_non_equal=cond_non_equal,
            cond_not_null=cond_not_null,
            cond_null=cond_null,
            silent=True,
        )
        ids_to_update_ls = [str(dt["id"]) for dt in ids_to_update]

        if not ids_to_update:
            self.logger.info("nothing to update")
            return tuple()

        args = list()
        query_parts = [f"UPDATE {table_name} SET"]

        query_set_part = list()
        for col_prev, col_new in update_col_col.items():
            query_set_part.append(f"{col_prev} = {col_new}")
        for col, value in update_col_value.items():
            query_set_part.append(f"{col} = %s")
            args.append(value)
        query_parts.append(", ".join(query_set_part))

        query_parts.append(f"WHERE id IN ({','.join(['%s']*len(ids_to_update_ls))})")
        args.extend(ids_to_update_ls)

        query_parts.append(";")

        self.execute(query=" ".join(query_parts), args=tuple(args), silent=silent)
        self.connection.commit()  # type: ignore

        return self.select(table_name=table_name, cond_in={"id": ids_to_update_ls})

    def update_by_id(
        self,
        table_name: str,
        id: str,
        update_col_col: dict[str, str] = dict(),
        update_col_value: dict[str, object] = dict(),
        silent=False,
    ) -> dict:
        """Update a single row in a table by its ID.

        Parameters
        ----------
        table_name : str
            Name of the table to update
        id : str
            ID of the row to update
        update_col_col : dict[str, str], optional
            Dictionary mapping columns to update with other column values
        update_col_value : dict[str, object], optional
            Dictionary mapping columns to update with specific values
        silent : bool, optional
            If True, suppress logging of the query execution, by default False

        Returns
        -------
        dict
            Updated row data, empty dict if row not found

        Raises
        ------
        NoConnectionError
            If no database connection exists
        DuplicateColumnUpdateError
            If a column appears in both update_col_col and update_col_value
        MySqlWrongQueryError
            If query is wrong
        """
        mysql_res = self.update(
            table_name=table_name,
            update_col_col=update_col_col,
            update_col_value=update_col_value,
            cond_equal={"id": id},
            silent=silent,
        )
        return mysql_res[0] if mysql_res else dict()

    def id_exists(
        self,
        table_name: str,
        id: str,
        silent: bool = False,
    ) -> bool:
        res = self.select_by_id(table_name=table_name, id=id, silent=silent)
        if res:
            return True
        return False
