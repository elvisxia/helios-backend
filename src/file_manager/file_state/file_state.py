import operator
from typing import TypedDict, Annotated

from langchain_core.messages import AnyMessage


class FileState(TypedDict):
    messages:Annotated[list[AnyMessage], operator.add]
    import_dir_path:str
    import_file_path:str
    file_name:str
    ext:str


