import os
from uuid import uuid4

from psycopg_pool import ConnectionPool








class PostgresDAO:
    def __init__(self,pool:ConnectionPool):
        self.pool = pool

    def save_memory(self,value:str,user_id:str):
        sql="""insert into public.memory (user_id,memory_id,raw) VALUES (%s,%s,%s)"""
        try:
            with self.pool.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        sql,
                        (user_id,uuid4(),value)
                    )
        except Exception as e:
            print(e)



if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    POSTGRES_URL = os.environ.get('POSTGRES_URL')
    pool = ConnectionPool(
        conninfo=POSTGRES_URL,
        min_size=1,
        max_size=20,
    )

    repo=MemoryRepository(pool)
    repo.save_memory(value='test',user_id='test')

    print("保存成功！！")