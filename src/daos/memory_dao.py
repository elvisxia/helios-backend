import os
from uuid import uuid4
from datetime import datetime


from utils.embedding_util import EmbeddingUtil


class MemoryDAO:
    def __init__(self,embedding_util,milvus_client):
        self.client=milvus_client
        self.embedding_util=embedding_util

    def save_memory(self,user_id:str,text:str):
        """
        save memroy user_id and text needs to be provided
        Args:
            user_id: user id
            text: memory text

        Returns:
            insert outcome
        """
        embedding=self.embedding_util.text_to_embedding(text)
        data={
            "id":str(uuid4()),
            "text":text,
            "embedding":embedding,
            "user_id":user_id,
            "create_time":str(datetime.now()),
            "update_time":str(datetime.now())
        }
        res=self.client.insert(
            collection_name="memory",
            data=data
        )
        return res

    def save_memories(self,user_id:str,texts:list):
        """
        save multiple memories user_id and texts needs to be provided
        Args:
            user_id: user id
            texts: memory texts

        Returns:
            insert outcome
        """
        embeddings=self.embedding_util.texts_to_embeddings(texts)
        data=list()
        for idx,embedding in enumerate(embeddings):
            data.append({
                "id":str(uuid4()),
                "text":texts[idx],
                "embedding":embedding,
                "user_id":user_id,
                "create_time":str(datetime.now()),
                "update_time":str(datetime.now())
            })
        res=self.client.insert(
            collection_name="memory",
            data=data
        )
        insert_count=res['insert_count']
        ids=res['ids']
        return res

    def del_memories(self,ids:list):
        """
        delete multiple memories, memories ids need to be provided
        Args:
            ids: memory ids

        Returns:
            delete count ex: {'delete_count': 2}
        """
        res=self.client.delete(
            collection_name="memory",
            ids=ids
        )
        print(res)

    def update_memory(self,id:str,text:str,user_id:str):
        """
        update the memory old memory id and new text needs to be provided，notice: the id will change after update
        Args:
            id:  memory id
            text: new text of the memory
            user_id: user id
        Returns:
            the updated memory id and update count ex: {'upsert_count': 1, 'ids': ['e7707f46-a0e9-492d-a823-74453e3483cc']}
        """
        embedding=self.embedding_util.text_to_embedding(text)
        data={
            "id":id,
            "text":text,
            "embedding":embedding,
            "user_id":user_id,
            "update_time":str(datetime.now())
        }
        res=self.client.upsert(
            collection_name="memory",
            data=[data]
        )
        print(res)
        return res

    def query_memory_byid(self,id:int):
        res=self.client.query(
            collection_name="memory",
            filter=f"id=={id}",
            output_fields=[
                "id",
                "text",
                "user_id",
                "create_time",
                "update_time"
            ]
        )

    def query_memories_by_userid(self,user_id:str):
        """
        query all memories by user id
        Args:
            user_id: user id
        Returns:
            all the user memories
        """
        res=self.client.query(
            collection_name="memory",
            filter=f"user_id=='{user_id}'",
            output_fields=[
                "id",
                "text",
                "user_id",
                "create_time",
                "update_time"
            ]
        )
        return res


    def search_memories(self,query:str,user_id:str):
        """
        search the memories by query and user id
        Args:
            query: query text
            user_id: user id
        Returns:
            all the searched memories
        """
        query_vector=self.embedding_util.text_to_embedding(query)
        res=self.client.search(
            collection_name="memory",
            filter=f"user_id=='{user_id}'",
            data=[query_vector],
            limit=5,
            output_fields=[
                "user_id",
                "text"
            ]
        )
        final_res=res[0]
        final=[item  for item in final_res if item['distance']>0.5]
        return final





if __name__ =="__main__":
    from utils.container import  container
    test_memories = [
        "我早上通常会喝一杯美式咖啡，不喜欢加糖。",
        "我平时比较喜欢在早上处理需要集中注意力的工作。",
        "工作累的时候，我习惯听音乐放松一下。",
        "我晚上睡觉前通常会看一会儿手机。",
        "周末的时候我通常会陪家人一起吃饭。",
        "我平时喜欢把重要的文件备份到 NAS 上。",
        "我习惯使用 VS Code 编写 Python 代码。",
        "开发项目时，我通常会使用 Docker 管理服务。",
        "我学习新技术的时候喜欢先看官方文档，再动手写代码。",
        "遇到不会的问题时，我通常会先自己搜索资料，然后再尝试解决。",
        "我平时喜欢使用 Python 做 AI 相关开发。",
        "我最近经常学习大语言模型和 Agent 相关技术。",
        "我习惯把正在学习的技术知识整理成笔记。",
        "我每天都会检查一下当天需要完成的任务。",
        "每周开始的时候，我通常会提前安排这一周的重要事情。",
        "出门的时候我习惯检查手机、钥匙和钱包有没有带。",
        "旅行之前我通常会提前检查身份证、充电器和充电宝。",
        "如果家里的网络突然变慢，我通常会先重启路由器。",
        "购买电子产品之前，我习惯先比较几个不同型号的产品。",
        "我比较喜欢把经常使用的工具和服务部署在自己的服务器上。",
    ]
    dao=container.memory_dao
    # test insert memories
    res=dao.save_memories(user_id="c404fa4e-8cdc-4b0b-8ea1-5ca862e042d5",texts=test_memories)

    # test update memory
    #res=dao.update_memory(id="e7707f46-a0e9-492d-a823-74453e3483cc",text="我早上通常会喝一杯美式咖啡，不喜欢加糖，但是喜欢加牛奶。",user_id="c404fa4e-8cdc-4b0b-8ea1-5ca862e042d5")

    # test delete memory and memories
    #to_del_ids=["ed96d194-9f1d-42e7-b5c6-4b5f96292d91","e7707f46-a0e9-492d-a823-74453e3483cc"]
    #dao.del_memories(to_del_ids)

    # test query memories
    #res=dao.query_memories_by_userid(user_id="c404fa4e-8cdc-4b0b-8ea1-5ca862e042d5")
    #print(res[0])

    # test search memories
    #res=dao.search_memories(query="我平时喜欢干什么？",user_id="c404fa4e-8cdc-4b0b-8ea1-5ca862e042d5")
    #print(res)




