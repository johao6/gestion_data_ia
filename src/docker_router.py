from typing import Optional, Dict, List

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

import os
import logging

logger = logging.getLogger(__name__)


class RunContainerRequest(BaseModel):
    image: str
    name: Optional[str] = None
    command: Optional[List[str]] = None
    detach: Optional[bool] = True
    ports: Optional[Dict[str, str]] = None


router = APIRouter()


def _get_docker_client():
    try:
        import docker

        docker_host = os.getenv("DOCKER_HOST")
        if docker_host:
            return docker.DockerClient(base_url=docker_host)
        return docker.from_env()
    except Exception as e:
        logger.debug("Docker client not available: %s", e)
        return None


@router.get("/containers")
def list_containers(all: bool = True):
    client = _get_docker_client()
    if client is None:
        raise HTTPException(status_code=503, detail="Docker daemon not available")

    containers = client.containers.list(all=all)
    result = []
    for c in containers:
        try:
            info = {
                "id": c.id,
                "name": c.name,
                "image": str(c.image.tags if hasattr(c.image, 'tags') else c.image),
                "status": c.status,
            }
        except Exception:
            info = {"id": getattr(c, 'id', None), "status": getattr(c, 'status', None)}
        result.append(info)
    return result


@router.get("/images")
def list_images():
    client = _get_docker_client()
    if client is None:
        raise HTTPException(status_code=503, detail="Docker daemon not available")

    images = client.images.list()
    return [", ".join(img.tags) if img.tags else img.short_id for img in images]


@router.post("/containers/run")
def run_container(req: RunContainerRequest):
    client = _get_docker_client()
    if client is None:
        raise HTTPException(status_code=503, detail="Docker daemon not available")

    try:
        # pull image (no error if exists)
        try:
            client.images.pull(req.image)
        except Exception:
            pass

        ports = None
        if req.ports:
            # expected mapping like {"8000/tcp": "8000"} or {"8000": "8000"}
            ports = req.ports

        container = client.containers.run(
            req.image,
            name=req.name,
            command=req.command,
            detach=req.detach,
            ports=ports,
        )
        return {"id": container.id, "status": getattr(container, 'status', 'created')}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/containers/{container_id}/start")
def start_container(container_id: str):
    client = _get_docker_client()
    if client is None:
        raise HTTPException(status_code=503, detail="Docker daemon not available")

    try:
        c = client.containers.get(container_id)
        c.start()
        return {"id": c.id, "status": c.status}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/containers/{container_id}/stop")
def stop_container(container_id: str):
    client = _get_docker_client()
    if client is None:
        raise HTTPException(status_code=503, detail="Docker daemon not available")

    try:
        c = client.containers.get(container_id)
        c.stop()
        return {"id": c.id, "status": c.status}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
