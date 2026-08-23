import uuid

from langgraph.types import interrupt

from file_manager.file_state.file_state import FileState
from llms.deepseek_llm import deepseek_llm
from utils.interrupt_value import InterruptValue


def handle_text_node(state:FileState):
    print(f"received text file:{state["file_name"]} with extension:{state['ext']}")
    file_name=state["file_name"]
    interrupt_value=InterruptValue(
        type="input",
        message=f"请给文件 {file_name} 添加注释：\n",
    )
    answer=interrupt(interrupt_value)
    return state