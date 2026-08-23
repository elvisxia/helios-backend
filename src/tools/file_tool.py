from langchain_core.tools import tool
from langgraph.prebuilt import ToolRuntime

from contexts.file_context import MainContext


class FileTools:
    def __init__(self,file_service):
        self.file_service = file_service

    def get_tools(self):

        @tool(name="save_file")
        def save_file(text:str,runtime:ToolRuntime[MainContext]):
            return None