import os
from multiprocessing import pool
from uuid import uuid4

from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool


class PostgresDB:
    _conn_str:str
    def __init__(self):
        _conn_str = os.environ.get('POSTGRES_URL')
        self.pool=ConnectionPool(
            conninfo=_conn_str,
            min_size=1,
            max_size=20,
        )

    def close(self):
        self.pool.close()

    def execute(self,sql:str,params:tuple|dict|None=None):
        """
        INSERT / UPDATE / DELETE
        Args:
            sql: sql command
            params: params

        Returns:
            conn.info

        """
        with self.pool.getconn() as conn:
            try:
                with conn.cursor() as cur:
                    cur.execute(sql,params)
                conn.commit()
                return conn.info
            except Exception as e:
                conn.rollback()
                raise e

    def fetch_one(self,sql: str,params: tuple | dict | None = None) -> dict | None:
        """
        Fetch one row only
        Args:
            sql: sql command
            params: params

        Returns:
            cursor.fetchone()
        """
        with self.pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute(sql, params)
                return cursor.fetchone()

    def fetch_all(self,sql: str,params: tuple | dict | None = None) -> list[dict]:
        """
        Fetch all rows
        Args:
            sql: sql command
            params: params

        Returns:
            cursor.fetchall()

        """
        with self.pool.getconn() as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute(sql, params)
                return cursor.fetchall()

    def fetch_value(self,sql:str,params: tuple | dict | None = None):
        """
        Fetch Count(*) Exists or sinle col
        Args:
            sql: sql command
            params: params

        Returns:
            cursor.fetchone()[0]
        """
        with self.pool.getconn() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, params)
                row=cursor.fetchone()
                if row is None:
                    return None
                return row[0]

    def execute_many(self,sql:str,params: tuple | dict | None = None):
        """
        execute many ex: INSERT INTO users (username)
                        VALUES
                            (%s),
                            (%s),
                            (%s)
                        RETURNING id, username;
        Args:
            sql: sql command
            params: params

        Returns:

        """
        with self.pool.getconn() as conn:
            with conn.cursor() as cursor:
                cursor.executemany(sql, params)
                conn.commit()


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()

    db=PostgresDB()
    res=db.execute_sql("select now()")
    print(res)

