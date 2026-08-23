from typing import TypedDict, Literal, Optional


class InterruptValue(TypedDict):
    # interrupt类型
    type: Literal[
        "approval",
        "input",
        "selection",
        "form",
        "review"
    ]
    # 给用户看的描述
    message: str

class ResponseValue(TypedDict):
    message:str