from langchain_core.language_models import BaseChatModel
from langchain_core.messages import HumanMessage

from llms.deepseek_llm import deepseek_llm


class LLMUtil:
    @classmethod
    def invoke(cls,prompt:str):
        res=deepseek_llm.invoke(prompt)
        return res


if __name__=="__main__":
    res=LLMUtil.invoke("你好")
    print(res)