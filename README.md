# gestion_data_ia

Instrucciones para usar Docker con este proyecto.

Construir la imagen:

# gestion_data_ia

Instrucciones para usar Docker con este proyecto.

Construir la imagen:

```powershell
docker build -t gestion_data_ia:latest .
```

Ejecutar con Docker:

```powershell
docker run --rm -it -p 8000:8000 gestion_data_ia:latest python -m http.server 8000
```

Usar docker-compose (desarrollo):

```powershell
docker-compose up --build
```

Si vas a usar el router Docker dentro del contenedor, el `docker-compose.yml` monta el socket del host y define `DOCKER_HOST=unix:///var/run/docker.sock`.

Notas:
- Si tiene `requirements.txt` en la raíz será instalado automáticamente.
- El contenedor añade `/app/src` al `PYTHONPATH`.
- Para que los endpoints de Docker funcionen dentro del contenedor, Docker Desktop debe estar activo y el socket del host debe montarse.

**Integración Continua / CI**

Este repositorio incluye un workflow de GitHub Actions en `.github/workflows/ci.yml` que realiza:
- Instalación de dependencias (si existe `requirements.txt`).
- Chequeo de sintaxis compilando `src/`.
- Construcción y push de la imagen Docker a GitHub Container Registry (GHCR) en `push`.

Para permitir push a GHCR no se requiere configuración adicional en la mayoría de repositorios públicos, pero puede que necesite ajustar permisos o tokens para repositorios privados. Para usar Docker Hub o despliegues automáticos configure los secretos correspondientes en el repo (`DOCKERHUB_USERNAME`, `DOCKERHUB_TOKEN`, etc.).

**Despliegue (sugerido)**

Opciones simples para desplegar la aplicación:
- Render: cree un servicio en Render conectado al repositorio y configure `Dockerfile` como método de despliegue. Añada variables de entorno (secrets) en el panel de Render.
- Supabase: útil si necesita base de datos Postgres y autenticación; despliegue la API/servicio externo (Render, Vercel) y conecte a la base de datos de Supabase mediante `DATABASE_URL` y `SUPABASE_KEY`.

Pasos recomendados para la actividad práctica en la nube:
1. Crear un repositorio en GitHub y subir este proyecto.
2. Habilitar GitHub Actions (ya incluído). Push a `main` para que el workflow construya la imagen.
3. Crear cuenta en Render o Supabase y configurar despliegue; añadir secretos necesarios en la interfaz de la plataforma.
4. Tomar capturas de pantalla del proceso (repositorio, acciones CI, panel de despliegue) y pegar URLs en este `README`.

**Archivos añadidos**
- `Dockerfile` — imagen base Python y comandos para instalar `requirements.txt`.
- `.dockerignore` — excluir artefactos.
- `docker-compose.yml` — servicio de desarrollo que expone el puerto 8000.
- `.gitignore` — reglas para Python y datos.
- `.env.example` — variables de entorno de ejemplo.
- `.github/workflows/ci.yml` — workflow CI que construye y sube la imagen a GHCR en `push`.

Si quieres, puedo:
- Ejecutar la construcción localmente (`docker build`) ahora.
- Configurar un pipeline de despliegue directo a Render o preparar plantillas específicas para Supabase.
