import time
import os
import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_core.messages import HumanMessage
from graph.agent import create_agent_graph

# ------------- #
# Phoenix Setup #
# ------------- #
import os
from phoenix.otel import register
from openinference.instrumentation.openai import OpenAIInstrumentor

collector_endpoint = os.environ.get("PHOENIX_COLLECTOR_ENDPOINT", "http://localhost:6006/v1/traces")
tracer_provider = register(
    endpoint=collector_endpoint,
    project_name="default",
    auto_instrument=True,
    batch=True
)
OpenAIInstrumentor().instrument(tracer_provider=tracer_provider)

# ------------- #
# FastAPI Setup #
# ------------- #
app = FastAPI(title="LLM Agent API", version="1.0")

# Esperar Ollama al inicio
@app.on_event("startup")
def startup_event():
    host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    print("Esperando a Ollama...")
    for _ in range(30):
        try:
            requests.get(f"{host}/api/tags", timeout=2)
            print("Ollama listo!")
            return
        except:
            time.sleep(2)
    raise RuntimeError("Ollama no responde")

# Crear grafo una vez
agent_app = create_agent_graph()

class ChatRequest(BaseModel):
    message: str
    thread_id: str = "default"

class ChatResponse(BaseModel):
    response: str
    tool_used: bool = False

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    config = {"configurable": {"thread_id": request.thread_id}}
    inputs = {"messages": [HumanMessage(content=request.message)]}

    final_state = None
    for event in agent_app.stream(inputs, config, stream_mode="values"):
        final_state = event

    if not final_state or not final_state["messages"]:
        raise HTTPException(status_code=500, detail="No response")

    last_msg = final_state["messages"][-1]
    tool_used = last_msg.type == "ai" and getattr(last_msg, "tool_calls", None)

    return ChatResponse(
        response=last_msg.content,
        tool_used=bool(tool_used)
    )
