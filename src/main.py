
import logging
import os  # Importación necesaria para el puerto
from fastapi import FastAPI
from .docker_router import router as docker_router

app = FastAPI(title="gestion_data_ia Docker API")
logger = logging.getLogger(__name__)

app.include_router(docker_router, prefix="/docker", tags=["docker"])

@app.get("/")
def read_root():
    return {"message": "API de Gestión de Data e IA operativa", "docs": "/docs"}

@app.get("/health")
def health():
    docker_available = False
    docker_error = None
    try:
        import docker
        docker_host = os.getenv("DOCKER_HOST")
        client = docker.DockerClient(base_url=docker_host) if docker_host else docker.from_env()
        try:
            client.api.ping()
            docker_available = True
        except Exception as e:
            docker_error = str(e)
    except Exception as e:
        docker_error = str(e)

    status = "ok" if docker_available else "degraded"
    return {"status": status, "docker_available": docker_available, "docker_error": docker_error}

# ESTO SIEMPRE AL FINAL
if __name__ == "__main__":
    import uvicorn
    # Lee el puerto de Render o usa 8000 por defecto
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("src.main:app", host="0.0.0.0", port=port, reload=True)