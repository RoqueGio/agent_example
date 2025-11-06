# LLM Agent con FastAPI + LangGraph + Ollama

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
Ingresar a la siguiente URL en un navegador.

```
http://127.0.0.1:8000/docs
```

---

### Comandos Útiles

```bash
# Ver logs
podman logs -f llm-agent

# Entrar al contenedor
podman exec -it llm-agent bash

```
