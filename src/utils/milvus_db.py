
import os

from pymilvus import MilvusClient



class MilvusDB:
    def __init__(self):
        DB_URI=os.environ.get("MILVUS_URI")
        DB_TOKEN=os.environ.get("MILVUS_TOKEN")
        DB_NAME=os.environ.get("MILVUS_DB")
        self.milvus_client=MilvusClient(
                    uri=DB_URI,
                    token=DB_TOKEN,
                    db_name=DB_NAME
                )