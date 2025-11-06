from langchain_ollama import ChatOllama
import os
from pathlib import Path

from tools.math_tools import add_numbers

def get_system_prompt():
    prompt_path = Path(__file__).parent.parent / "prompts" / "system.txt"
    if not prompt_path.exists():
        return "Eres un agente útil que responde siempre en español."
    return prompt_path.read_text(encoding="utf-8").strip()

def get_llm():
    host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    # system_prompt = get_system_prompt()
    llm = ChatOllama(
        model="llama3.1:8b",
        base_url=host,
        temperature=0,
        # system=system_prompt
    )
    llm.bind_tools([add_numbers])
    return llm
