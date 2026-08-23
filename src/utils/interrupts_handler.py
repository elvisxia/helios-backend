from typing import List

from langgraph.errors import GraphInterrupt

from utils import interrupt_value
from utils.interrupt_value import InterruptValue,ResponseValue


class InterruptsHandler:
    @staticmethod
    def handle_interrupts(interrupts:List[GraphInterrupt])->dict:
        ans={}
        for interrupt in interrupts:
            interrupt_value=InterruptValue(**interrupt.value)
            cur_ans=input(interrupt_value["message"])
            ans[interrupt.id]=cur_ans
        return ans