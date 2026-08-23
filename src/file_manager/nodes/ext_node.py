import pathlib

def handle_ext_node(state:dict):
    """
    获取文件的后缀，文件名以及其他信息
    Args:
        state:
    Returns:

    """
    print("state",state)
    file_path=pathlib.Path(state["file_name"])
    ext=file_path.suffix
    dir_path=file_path.__dir__()
    return {
        "file_name":file_path.name,
        "ext":file_path.suffix.lower(),
        "import_dir_path":str(file_path.parent),
        "import_file_path":str(file_path),
    }
