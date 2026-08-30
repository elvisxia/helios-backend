from uuid import uuid4
from datetime import datetime

from app.models.dao.file_meta import FileMeta
from utils.embedding_util import EmbeddingUtil


class FileMetaDao:
    def __init__(self,milvus_client):
        self.client=milvus_client

    def save_file_meta(self,text:str,file_path:str,user_id:str):
        embedding=EmbeddingUtil.text_to_embedding(text)
        data={
            "id":str(uuid4()),
            "embedding":embedding,
            "text":text,
            "file_path":file_path,
            "user_id":user_id,
            "create_time":str(datetime.now())
        }
        res = self.client.insert(
            collection_name="file",
            data=data
        )
        return res

    def save_file_metas(self,file_metas:list[FileMeta]):
        rows=[fm.model_dump() for fm in file_metas]
        res=self.client.insert(
            collection_name="file",
            data=rows
        )
        return res

    # def save_file_metas(self,text_list:list,file_path_list:list,user_id:str):
    #     embeddings=EmbeddingUtil.text_to_embedding(text_list)
    #     data=list()
    #     for idx,item in enumerate(embeddings):
    #         data.append({
    #             "id":str(uuid4()),
    #             "embedding":item,
    #             "text":text_list[idx],
    #             "user_id":user_id,
    #             "file_path":file_path_list[idx],
    #             "create_time":str(datetime.now()),
    #         })
    #     res=self.client.insert(
    #         collection_name="file",
    #         data=data)
    #     return res

    def update_file_meta(self,id:str,new_text:str,new_file_path:str,user_id:str):
        embedding=EmbeddingUtil.text_to_embedding(new_text)
        data={
            "id":id,
            "embedding":embedding,
            "text":new_text,
            "file_path":new_file_path,
            "user_id":user_id,
            "create_time":str(datetime.now())
        }
        res=self.client.upsert(
            collection_name="file",
            data=data
        )
        return res

    def delete_file_meta(self,ids=list[str]):
        res=self.client.delete(
            collection_name="file",
            ids=ids
        )
        return res

    def search_file_meta(self,text:str,user_id:str):
        search_embedding=EmbeddingUtil.text_to_embedding(text)
        res=self.client.search(
            collection_name="file",
            filter=f"user_id == '{user_id}'",
            data=[search_embedding],
            limit=5,
            output_fields=[
                "id",
                "text",
                "file_path",
                "user_id",
                "create_time"
            ]
        )
        final_res = res[0]
        final = [item for item in final_res if item['distance'] > 0.5]
        return final


if __name__ =="__main__":
    from utils.container import container
    dao=container.file_milvus_dao
    #res=dao.save_file_meta(text="测试文件",file_path="test/test.pdf",user_id="c404fa4e-8cdc-4b0b-8ea1-5ca862e042d5")

    #测试多个稳健插入
    # text_list=["第一个测试文件","第二个测试文件","第三个测试文件"]
    # file_path_list=["test/test.pdf","test/test2.pdf","test/test3.pdf"]
    # user_id="c404fa4e-8cdc-4b0b-8ea1-5ca862e042d5"
    # res=dao.save_file_metas(text_list=text_list,file_path_list=file_path_list,user_id=user_id)
    # print(res)

    #测试更新
    # id="8f9f29a2-9f2e-4647-9cd3-8956581fc4c9"
    # text="更改后的测试文件"
    # user_id = "c404fa4e-8cdc-4b0b-8ea1-5ca862e042d5"
    # new_file_path="test/test_new.pdf"
    # user_id = "c404fa4e-8cdc-4b0b-8ea1-5ca862e042d5"
    # res=dao.update_file_meta(id=id,new_text=text,new_file_path=new_file_path,user_id=user_id)
    # print(res)

    #删除测试
    # ids=["bce271bd-55cf-4389-8978-0f05af350d5e","3022f553-a160-4a92-b740-db81543b1de3"]
    # res=dao.delete_file_meta(ids=ids)
    # print(res)

    #测试search
    user_id="c404fa4e-8cdc-4b0b-8ea1-5ca862e042d5"
    res=dao.search_file_meta(text="测试文件",user_id=user_id)
    print(res)