import logging

from fastapi import FastAPI

from .docker_router import router as docker_router


app = FastAPI(title="gestion_data_ia Docker API")

logger = logging.getLogger(__name__)

app.include_router(docker_router, prefix="/docker", tags=["docker"])


@app.get("/health")
def health():
	"""Health check endpoint.

	Returns application health and Docker daemon availability separately.
	"""
	docker_available = False
	docker_error = None
	try:
		import docker

		docker_host = None
		import os

		docker_host = os.getenv("DOCKER_HOST")
		client = docker.DockerClient(base_url=docker_host) if docker_host else docker.from_env()
		# docker-py exposes ping() on low-level API
		try:
			client.api.ping()
			docker_available = True
		except Exception as e:
			docker_error = str(e)
	except Exception as e:
		docker_error = str(e)

	status = "ok" if docker_available else "degraded"
	return {"status": status, "docker_available": docker_available, "docker_error": docker_error}


if __name__ == "__main__":
	import uvicorn

	uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)

