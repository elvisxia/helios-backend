from langgraph.constants import END

from file_manager.file_state.file_state import FileState
from file_manager.nodes.node_names import File_Node_Names


def handle_ext_edge(state:FileState):
    ext=state["ext"]
    print("ext:",ext)
    if not ext:
        return END
    else:
        if ext==".txt":
            return File_Node_Names.HANDLE_TEXT_NODE
        if ext in [".jpeg",".jpg",".png"]:
            return File_Node_Names.HANDLE_IMAGE_NODE