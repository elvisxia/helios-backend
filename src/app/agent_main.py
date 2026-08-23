from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.memory import InMemorySaver

from contexts.main_context import Context
from llms.deepseek_llm import deepseek_llm
from utils.container import Container
from langfuse.langchain import CallbackHandler

from utils.environment_util import load_env

checkpointer=InMemorySaver()

container=Container()

tools=container.memory_tools.get_tools()

agent=create_agent(
    model=deepseek_llm,
    checkpointer=checkpointer,
    tools=tools,
    context_schema=Context
)



if __name__=="__main__":
    load_env()
    langfuse_handler=CallbackHandler()
    config=RunnableConfig(
        configurable={
            "thread_id":"test-user-001"
        },
        callbacks=[langfuse_handler]
    )
    context=Context(
        user_id="c404fa4e-8cdc-4b0b-8ea1-5ca862e042d5"
    )
    result=agent.invoke(
        {"messages":[HumanMessage(content="给我更新我不喜欢健身相关的memory，我现在又喜欢健身了")]},
        config=config,
        context=context,
    )
    print(result["messages"])