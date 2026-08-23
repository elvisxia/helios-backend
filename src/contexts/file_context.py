from dataclasses import dataclass
from typing import TypedDict

@dataclass
class FileContext:
    user_id:str

@dataclass
class MainContext:
    user_id:str