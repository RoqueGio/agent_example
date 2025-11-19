# LLM Agent con FastAPI + LangGraph + Ollama + Phoenix

## Iniciar

```bash
podman-compose up -d
```

## Detener

```bash
podman-compose down
```

## Primer uso (descargar modelo)

```bash
podman-compose up -d --build
podman exec -it ollama ollama pull llama3.1:8b
```

## Probar
Para probar la API con FastAPI:

```
http://127.0.0.1:8000/docs
```

Para observability con Phoenix:

```
http://127.0.0.1:6006
```

---

### Comandos Útiles

```bash
# Ver logs
podman logs -f llm-agent

# Entrar al contenedor
podman exec -it llm-agent bash

```
