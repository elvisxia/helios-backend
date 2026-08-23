from langchain_core.language_models import BaseChatModel
from langchain_core.messages import HumanMessage

from llms.deepseek_llm import deepseek_llm


class LLMUtil:
    def __init__(self,model):
        self.model=model

    def query(self,prompt:str):
        res=self.model.invoke(prompt)
        return res


if __name__=="__main__":
    llm_service=LLMUtil(model=deepseek_llm)
    res=llm_service.query("你好")
    print(res)