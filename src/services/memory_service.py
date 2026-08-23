from utils.prompt_util import PromptUtil
import ast

class MemoryService:
    def __init__(self,memory_dao,llm_util):
        self.memory_dao= memory_dao
        self.llm_util = llm_util

    def save_memories(self,user_id:str,text:str):
        """
        save user's memory
        Args:
            user_id: user id
            text: user's input
        Returns:
            save result
        """
        # 1. extract memories list using llm
        extracted_result=self.extract_memories(text)
        # 2. save memories using milvus dao
        res=self.memory_dao.save_memories(user_id,ast.literal_eval(extracted_result.content))
        return res
        # if res['insert_count'] and res['insert_count']>0:
        #     return "save memory successfully"
        # else:
        #     return "something went wrong in remember service!!"

    def search_memory(self,user_id:str,text:str):
        """
        search user's memory
        Args:
            user_id: user id
            text: user search text

        Returns:
            search result
        """
        result=self.memory_dao.search_memories(query=text,user_id=user_id)
        return result

    def update_memory(self,user_id:str,old_text:str,new_text:str):
        """
        update user's memory
        Args:
            user_id: user id
            old_text: 原本的记忆内容
            new_text: 新的要更新的记忆内容

        Returns:

        """
        existing_memory=self.memory_dao.search_memories(query=old_text,user_id=user_id)
        if existing_memory and len(existing_memory)>0:
            existing_memory=[item for item in existing_memory if item['distance']>0.7]
        for memory in existing_memory:
            res=self.memory_dao.update_memory(id=memory['id'],text=new_text,user_id=user_id)
        return res

    def delete_memory(self,user_id:str,text:str):
        """
        delete user's memories
        Args:
            user_id: user id
            text: user's input

        Returns:

        """

    def extract_memories(self,text:str):
        # 1. get prompt from yaml file
        prompt_template=PromptUtil.get_prompt_from_yaml("memory_prompts.yaml","memory_extraction")
        prompt=prompt_template.format(input=text)
        # 2. get memory list using llm
        res=self.llm_util.query(prompt)
        return res



if __name__ == "__main__":
    from utils.container import container
    memory_service=container.memory_service
    #memory_service.extract_memories("我晚上睡觉前通常会看一会儿手机学习新技术的时候喜欢先看官方文档，再动手写代码出门的时候我习惯检查手机、钥匙和钱包有没有带家里的网络突然变慢，我通常会先重启路由器")
    res=memory_service.update_memory(user_id="c404fa4e-8cdc-4b0b-8ea1-5ca862e042d5",old_text="我喜欢健身",new_text="我现在不喜欢健身了")
    print(res)
