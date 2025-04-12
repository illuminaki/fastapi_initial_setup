
# FastAPI Hola Mundo

Este repositorio es un tutorial teórico e ilustrativo sobre [FastAPI](https://fastapi.tiangolo.com/), un framework moderno y de alto rendimiento para construir APIs con Python 3.7+ basado en estándares como OpenAPI y JSON Schema.

Incluye un ejemplo básico de "Hola Mundo" dockerizado, junto con explicaciones detalladas para principiantes sobre el funcionamiento de FastAPI, su estructura y despliegue.

---

## 🌟 Objetivos
- Entender los fundamentos básicos de FastAPI.
- Mostrar cómo estructurar una aplicación FastAPI.
- Ejecutar un ejemplo funcional de "Hola Mundo".
- Dockerizar una app FastAPI para entornos de desarrollo.

---

## 📁 Estructura del Repositorio
```
fastapi-hola-mundo/
├── app/
│   ├── __init__.py
│   └── main.py                # Archivo principal con la instancia de FastAPI
├── docs/
│   ├── introduction.md        # Introducción teórica a FastAPI
│   ├── fastapi_basics.md      # Conceptos básicos del framework
│   ├── docker_setup.md        # Guía para configurar Docker
│   └── example_usage.md       # Ejemplo práctico de uso
├── Dockerfile                 # Imagen base de FastAPI
├── docker-compose.yml         # Orquestación del contenedor
├── requirements.txt           # Dependencias del proyecto
├── README.md
└── .gitignore
```

---

## 🚀 Requisitos
Antes de iniciar la aplicación, asegúrese de tener instalado en su sistema:

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

---

## 📚 Primeros Pasos

### 1. Clonar el Repositorio
```bash
git clone https://github.com/illuminaki/fastapi-hola-mundo.git
cd fastapi-hola-mundo
```

### 2. Construir y levantar la aplicación con Docker Compose
```bash
docker compose up --build
```
Esto construirá la imagen Docker y levantará el contenedor. La aplicación estará disponible en:

- API: [http://localhost:8000](http://localhost:8000)
- Documentación interactiva (Swagger UI): [http://localhost:8000/docs](http://localhost:8000/docs)
- Documentación alternativa (ReDoc): [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## ❌ Detener la Aplicación
Para detener la aplicación y eliminar los contenedores, ejecute:
```bash
docker compose down
```

Si desea eliminar también los volúmenes asociados (datos persistentes):
```bash
docker compose down -v
```

---

## 📄 Archivos Clave

### `app/main.py`
Ejemplo básico de FastAPI:
```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"mensaje": "Hola Mundo desde FastAPI"}
```

### `Dockerfile`
```Dockerfile
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

COPY ./app /app
```

### `docker-compose.yml`
```yaml
version: '3.9'
services:
  fastapi:
    build: .
    ports:
      - "8000:80"
    volumes:
      - ./app:/app
```

---

## 🔧 Dependencias
Las dependencias del proyecto se encuentran en `requirements.txt`. Puede instalar localmente con:
```bash
pip install -r requirements.txt
```

---

## 📅 Futuras Extensiones
- Autenticación JWT
- Conexión a base de datos
- Tests automáticos
- Deploy en servicios cloud

---

## ✨ Contribuciones
¡Las contribuciones son bienvenidas! Puedes abrir un issue o hacer un pull request si deseas aportar mejoras.

---

## 👁️ Licencia
Este repositorio está licenciado bajo la MIT License. Consulta el archivo [LICENSE](LICENSE) para más detalles.

---

