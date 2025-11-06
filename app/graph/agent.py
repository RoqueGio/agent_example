from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

from nodes.state import AgentState
from nodes.agent_node import agent_node
from nodes.tool_node import tool_node

def create_agent_graph():
    graph = StateGraph(AgentState)
    graph.add_node("agent", agent_node)
    graph.add_node("tools", tool_node)
    graph.set_entry_point("agent")

    def should_continue(state: AgentState):
        last_msg = state["messages"][-1]
        return "tools" if hasattr(last_msg, "tool_calls") and last_msg.tool_calls else END

    graph.add_conditional_edges("agent", should_continue)
    graph.add_edge("tools", "agent")

    memory = MemorySaver()
    return graph.compile(checkpointer=memory)
