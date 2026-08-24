from daos.file_dao import FileDAO
from daos.file_meta_dao import FileMetaDao
from daos.users_dao import UsersDAO
from infra.postgres_db import PostgresDB
from llms.deepseek_llm import deepseek_llm
from services.file_service import FileService
from services.memory_service import MemoryService
from services.user_service import UserService
from tools.file_tool import FileTools
from tools.memory_tool import MemoryTools
from utils.embedding_util import EmbeddingUtil
from daos.memory_dao import MemoryDAO
from utils.llm_util import LLMUtil
from infra.milvus_db import MilvusDB
from infra.minio_db import MinIODB


class Container:
    _instance=None
    def __init__(self):
        #db connections
        _milvus_client=MilvusDB().milvus_client
        _minio_client=MinIODB().minio_client
        _postgres_client=PostgresDB()
        #utils
        self.embedding_util=EmbeddingUtil()
        self.llm_util=LLMUtil(model=deepseek_llm)
        #daos
        self.memory_dao = MemoryDAO(self.embedding_util,
                                    _milvus_client)
        self.file_dao=FileDAO(_minio_client)
        self.file_meta_dao=FileMetaDao(milvus_client=_milvus_client,embedding_util=self.embedding_util)
        self.users_dao=UsersDAO(postgresDB=_postgres_client)
        #services
        self.memory_service = MemoryService(self.memory_dao,self.llm_util)
        self.file_service=FileService(file_meta_dao=self.file_meta_dao,file_dao=self.file_dao)
        self.user_service=UserService(userDAO=self.users_dao)
        #tools
        self.memory_tools=MemoryTools(
            self.memory_service
        )
        self.file_tool=FileTools(
            self.file_service
        )


    def __new__(self,*args, **kwargs):
        if Container._instance is None:
            Container._instance=object.__new__(self)
        return Container._instance


container=Container()


if __name__ == "__main__":
    container.milvus_client=MilvusDB()