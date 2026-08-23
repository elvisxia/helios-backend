from file_manager.nodes.ext_node import handle_ext_node
from file_manager.nodes.image_node import handle_image_node
from file_manager.nodes.node_names import File_Node_Names
from file_manager.nodes.text_node import handle_text_node

NODE_REGISTRY={
    File_Node_Names.HANDLE_EXT_NODE:handle_ext_node,
    File_Node_Names.HANDLE_TEXT_NODE:handle_text_node,
    File_Node_Names.HANDLE_IMAGE_NODE:handle_image_node
}