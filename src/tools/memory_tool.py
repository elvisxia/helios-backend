from os import name

from fastmcp.tools import tool
from langgraph.prebuilt import ToolRuntime
from scripts.regsetup import description

from contexts.file_context import MainContext

class MemoryTools:
    def __init__(self,memory_service):
        self.memory_service=memory_service

    def get_tools(self):
        @tool(name="save_memory")
        def save_memory(text:str,runtime:ToolRuntime[MainContext]):
            """
            保存用户要求记住的内容
            Args:
                text:用户的输入文本
                runtime: 工具运行时
            Returns:
                返回插入后的结果
            """
            user_id=runtime.context.user_id
            memory_service=self.memory_service
            result=memory_service.save_memories(user_id=user_id,text=text)
            return result

        @tool(name="search memory")
        def search_memory(text:str,runtime:ToolRuntime[MainContext]):
            """
            搜索用户的记忆
            Args:
                text: 用户输入的搜索memory的内容
                runtime: 工具运行时

            Returns:
                返回搜索的结果
            """
            user_id=runtime.context.user_id
            memory_service=self.memory_service
            result=memory_service.search_memory(user_id=user_id,text=text)
            return result

        @tool(name="update_memory")
        def update_memory(old_text:str,new_text:str,runtime:ToolRuntime):
            """
            更改用户的的记忆，需要提供memory_id和旧的记忆内容和新的记忆内容
            Args:
                id: memory id
                old_text: 旧的记忆内容
                new_text: 新的记忆内容
                runtime: 工具运行时

            Returns:
                更新的结果
            """
            user_id = runtime.context.user_id
            memory_service = self.memory_service
            result=memory_service.update_memory(old_text=old_text,new_text=new_text,user_id=user_id)
            return result

        return [
            save_memory,
            search_memory,
            update_memory,
        ]
    