import os
from encodings import utf_8

import yaml



def load_prompt_template(path:str):
    with open(path, "r",encoding="utf_8") as f:
        return yaml.safe_load(f)


if __name__ == "__main__":
    resp=load_prompt_template("../../prompts/file_prompts.yaml")
    res=resp["file_summary"].format(file_name="abc.txt",file_path="d:/abc/abc.txt")
    print(res)



