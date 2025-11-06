from langchain_core.messages import HumanMessage, SystemMessage
from nodes.state import AgentState

from model.llm import get_llm
from tools.math_tools import add_numbers
from model.llm import get_llm, get_system_prompt

_llm = get_llm()
_system_prompt = get_system_prompt()
_system_message = SystemMessage(content=_system_prompt)

def agent_node(state: AgentState):
    # Si es el primer mensaje del usuario, inyectar system prompt
    if len(state["messages"]) == 1 and isinstance(state["messages"][0], HumanMessage):
        messages = [_system_message] + state["messages"]
    else:
        messages = state["messages"]
    
    response = _llm.invoke(messages)
    return {"messages": [response]}
