import sqlite3
import psycopg2
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor
from db_cursors import PostgresSaver, SQLiteLoader
from dataclasses import astuple


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
    postgres_saver = PostgresSaver(pg_connection)
    # migrate each table
    for table in sqlite_loader.get_db_tables():
        # reset offset value
        offset = 0
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
                prepared_row = postgres_saver.cursor.mogrify(formatting, value).decode()
                values += f"\n({prepared_row}),"
            # save data in table
            postgres_saver.save_data(table=table, values=values)
            # update offset
            offset += chunk_n


if __name__ == "__main__":
    dsl = {
        "dbname": "movies",
        "user": "movies",
        "password": "movies",
        "host": "localhost",
        "port": 5432,
        "options": "-c search_path=content",
    }
    with sqlite3.connect("db.sqlite") as sqlite_conn, psycopg2.connect(
            **dsl, cursor_factory=DictCursor
    ) as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn)
