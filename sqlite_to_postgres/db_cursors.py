import sqlite3

import table_dataclasses as tdt

table_dataclasses: dict[str, object] = {
    "genre": tdt.Genre,
    "film_work": tdt.FilmWork,
    "person": tdt.Person,
    "genre_film_work": tdt.GenreFilmWork,
    "person_film_work": tdt.PersonFilmWork,
}


table_fields: dict[str, str] = {
    "genre": "id, created_at, updated_at, name, description",
    "film_work": "id, created_at, updated_at, title, type, file_path, description, certificate, creation_date, rating",
    "person": "id, created_at, updated_at, full_name, birth_date",
    "genre_film_work": "id, created_at, film_work_id, genre_id",
    "person_film_work": "id, created_at, film_work_id, person_id, role",
}


def postgres_save_data(cursor, table: str, values: str):
    """
    Save values in specific table in PostgreSQL database
    :param cursor: postgres cursor
        postgres db cursor
    :param table: str
        table's name in database
    :param values: str
        values for insert
    :return None
    """
    fields: str = table_fields.get(table)
    sql: str = f"""
    INSERT INTO content.{table} ({fields})
    VALUES {values[:-1]}
    ON CONFLICT DO NOTHING
    """
    return cursor.execute(sql)


class SQLiteLoader:
    """Class to load data from database"""

    def __init__(self, sqlite_conn: sqlite3.Connection):
        """Initialize sqlite db cursor"""
        self.cursor = sqlite_conn.cursor()

    @staticmethod
    def get_instance_dataclass(table: str, instance: tuple):
        """
        Return dataclass instance
        :param table: str
            table's name in database
        :param instance: tuple
            table instance
        :return table's dataclass
        """
        return table_dataclasses.get(table)(*instance)

    def get_tables_rows_count(self, table: str) -> int:
        """
        :return count of records in specific table
        """
        sql: str = f"SELECT COUNT(id) FROM {table}"
        return self.cursor.execute(sql).fetchone()[0]

    def get_formatting_string(self, table: str) -> str:
        """
        :return formatting string by count of table columns
        :example: "%s, %s, %s, %s"
        """
        sql: str = f"PRAGMA table_info({table})"
        count_of_columns: int = len(self.cursor.execute(sql).fetchall())
        return ", ".join(["%s" for i in range(count_of_columns)])

    def get_db_tables(self) -> list:
        """
        :return list of tables name
        """
        list_of_tables: list = [
            _tuple[0]
            for _tuple in self.cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table';"
            ).fetchall()
        ]
        return list_of_tables

    def get_data_by_table(self, table: str, limit: int, offset: int):
        """
        Method to get records from specific table
        :param table: str
            table's name in database
        :param limit: int
            count of objects
        :param offset: int
            starting from record
        :return db query
        """
        fields: str = table_fields.get(table)
        sql: str = f"SELECT {fields} FROM {table} LIMIT {limit} OFFSET {offset}"
        return self.cursor.execute(sql)
