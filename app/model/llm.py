from langchain_openai import ChatOpenAI
import os
from pathlib import Path

from tools import tool_list

def get_system_prompt():
    prompt_path = Path(__file__).parent.parent / "prompts" / "system.txt"
    if not prompt_path.exists():
        return "Eres un agente útil que responde siempre en español."
    return prompt_path.read_text(encoding="utf-8").strip()

def get_llm():
    host = os.getenv("OLLAMA_HOST", "http://localhost:11434/v1")
    llm = ChatOpenAI(
        base_url=host,
        api_key="ollama",
        model="llama3.1:8b",
    )
    llm = llm.bind_tools(tool_list)
    return llm
