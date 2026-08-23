import asyncio

from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.constants import START, END
from langgraph.graph import StateGraph
from langgraph.types import Command

from contexts.file_context import FileContext
from file_manager.edges.file_ext_edge import handle_ext_edge
from file_manager.file_state.file_state import FileState
from file_manager.nodes.node_names import File_Node_Names
from file_manager.nodes.node_registry import NODE_REGISTRY
from utils.interrupt_value import InterruptValue
from utils.interrupts_handler import InterruptsHandler


async def file_graph_main():
    builder = StateGraph(state_schema=FileState,
                         context_schema=FileContext)

    for key,node in NODE_REGISTRY.items():
        builder.add_node(key,node)

    builder.add_edge(START,File_Node_Names.HANDLE_EXT_NODE)
    builder.add_conditional_edges(source=File_Node_Names.HANDLE_EXT_NODE,
                                  path=handle_ext_edge,
                                  path_map=[
        File_Node_Names.HANDLE_TEXT_NODE,
        File_Node_Names.HANDLE_IMAGE_NODE,
        END])
    #set up config
    file_config={
        "configurable":{
            "thread_id":"session01"
        }
    }
    #set up context
    file_context=FileContext(user_id="user_001")
    #set up memory
    checkpointer=InMemorySaver()
    #build the graph
    file_graph=builder.compile(checkpointer=checkpointer)

    stream=file_graph.stream_events({"messages":[HumanMessage(content="你好")],"file_name":"D://abc/test.txt"},
                                   context=file_context,
                                   config=file_config,
                                   version="v3")
    if stream.interrupts:
        responses=InterruptsHandler.handle_interrupts(interrupts=stream.interrupts)
        resumed=file_graph.stream_events(Command(resume=responses),
                                         context=file_context,
                                         config=file_config,
                                         version="v3")
    print("resumed:",resumed.output)
    # res=file_graph.invoke({"messages":[HumanMessage(content="你好")],"file_name":"D://abc/test.txt"},
    #                       context=file_context,
    #                       config=file_config)
    #print("res:",res)

if __name__ == '__main__':
    asyncio.run(file_graph_main())