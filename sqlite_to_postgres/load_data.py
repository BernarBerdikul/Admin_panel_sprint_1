import os
import sqlite3
from dataclasses import astuple
from typing import Union

import psycopg2
from db_cursors import SQLiteLoader, postgres_save_data
from dotenv import load_dotenv
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor

load_dotenv()


def load_from_sqlite(
    sqlite_connection: sqlite3.Connection, pg_connection: _connection
) -> None:
    """
    Method to migrate data from SQLite to Postgres
    :return None
    """
    # number of objects to migrate
    chunk_n: int = 200
    # declare db cursors
    sqlite_loader = SQLiteLoader(sqlite_connection)
    postgres_cursor = pg_connection.cursor()
    # migrate each table
    for table in sqlite_loader.get_db_tables():
        # reset offset value
        offset: int = 0
        # get count of records in table
        count_obj = sqlite_loader.get_tables_rows_count(table=table)
        formatting = sqlite_loader.get_formatting_string(table=table)
        # declare count of data load waves
        count_of_waves: int = count_obj // chunk_n
        if count_obj % chunk_n != 0:
            count_of_waves += 1
        # run waves
        for wave in range(count_of_waves):
            # reset 'values' string
            values: str = ""
            for row in sqlite_loader.get_data_by_table(
                table=table, limit=chunk_n, offset=offset
            ):
                value: tuple = astuple(
                    sqlite_loader.get_instance_dataclass(table=table, instance=row)
                )
                prepared_row = postgres_cursor.mogrify(formatting, value).decode()
                values += f"\n({prepared_row}),"
            # save data in table
            postgres_save_data(cursor=postgres_cursor, table=table, values=values)
            # update offset
            offset += chunk_n


if __name__ == "__main__":
    dsl: dict[str, Union[str, int]] = {
        "dbname": os.getenv("DB_NAME"),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
        "host": os.getenv("DB_HOST", "127.0.0.1"),
        "port": os.getenv("DB_PORT", 5432),
        "options": "-c search_path=content",
    }
    sqlite_conn = sqlite3.connect("db.sqlite")
    pg_conn = psycopg2.connect(**dsl, cursor_factory=DictCursor)
    try:
        with sqlite_conn, pg_conn:
            load_from_sqlite(sqlite_conn, pg_conn)
    except Exception as e:
        raise e
    finally:
        sqlite_conn.close()
        pg_conn.close()
