from nodes.state import AgentState
from tools.math_tools import add_numbers
from langchain_core.messages import AIMessage

def tool_node(state: AgentState):
    last_msg = state["messages"][-1]
    tool_calls = getattr(last_msg, "tool_calls", [])
    results = []
    for tc in tool_calls:
        if tc["name"] == "add_numbers":
            result = add_numbers.invoke(tc["args"])
            results.append(AIMessage(content=str(result), tool_call_id=tc["id"]))
    return {"messages": results}
