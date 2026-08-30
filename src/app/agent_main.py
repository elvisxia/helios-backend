import asyncio
from uuid import uuid4

from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.memory import InMemorySaver

from contexts.main_context import Context
from llms.deepseek_llm import deepseek_llm
from utils.container import Container
from langfuse.langchain import CallbackHandler

from utils.environment_util import load_env
from utils.prompt_util import PromptUtil


class MainAgent:
    def __init__(self,user_id:str):
        self.llm=deepseek_llm
        self.checkpointer=InMemorySaver()
        self.container=Container()
        self.tools=[]
        self.tools.extend(self.container.memory_tools.get_tools())
        self.tools.extend(self.container.file_tools.get_tools())
        self._system_prompt=PromptUtil.get_prompt_from_yaml(yaml_file="system_prompts.yaml",title="system_prompt")
        self.agent=create_agent(
            model=self.llm,
            checkpointer=self.checkpointer,
            tools=self.tools,
            context_schema=Context,
            system_prompt=self._system_prompt,
        )
        self._langfuse_handler = CallbackHandler()
        self._config = RunnableConfig(
            configurable={
                "thread_id": str(uuid4())
            },
            callbacks=[self._langfuse_handler]
        )
        self._context = Context(
            user_id=user_id,
        )

    def invoke(self,text:str):
        return self.agent.invoke({"messages":[HumanMessage(content=text)]},
                          config=self._config,
                          context=self._context,
                          )

    async def stream_async(self,text:str):
        async for chunk,metadata in self.agent.astream(
                input={"messages":[HumanMessage(content=text)]},
                stream_mode="messages",
                config=self._config,
                context=self._context):
                yield chunk






if __name__=="__main__":
    load_env()

    user_id="c404fa4e-8cdc-4b0b-8ea1-5ca862e042d5"
    agent=MainAgent(user_id)
    result=agent.invoke(
        text="给我更新我不喜欢健身相关的memory，我现在又喜欢健身了"
    )
    print(result["messages"])