from langchain_core.tools import tool
from langgraph.prebuilt import ToolRuntime

from contexts.file_context import MainContext


class FileTools:
    def __init__(self,file_service):
        self.file_service = file_service

    def get_tools(self):

        @tool(name_or_callable="save_file_metas")
        def save_file_metas(text:str,attachments:list[str],runtime:ToolRuntime[MainContext]):
            """
                保存文件的meta data信息
                仅当用户明确要求保存、记录、归档、记住附件时，保存附件元信息。
                如果用户只是打招呼、闲聊、提问、让你查看/分析附件，不要调用此工具。
            Args:
                text: 用户输入信息
                attachments: 文件列表
                runtime: 工具运行时

            Returns:
                工具返回结果，保存成功还是失败
            """
            #save_files_metas(self,file_list:list[str],text:str,user_id:str):
            user_id=runtime.context.user_id
            res=self.file_service.save_file_metas(file_list=attachments,text=text,user_id=user_id)
            return res

        return [
            save_file_metas,
        ]