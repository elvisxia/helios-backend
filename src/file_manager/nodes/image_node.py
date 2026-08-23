from file_manager.file_state.file_state import FileState


def handle_image_node(state:FileState):
    print(f"received image file:{state["file_name"]} with extension:{state['ext']}")
    return state