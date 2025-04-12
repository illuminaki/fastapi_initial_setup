# Conceptos Básicos de FastAPI

## Historia y Origen de FastAPI

FastAPI fue creado por Sebastián Ramírez (conocido como "tiangolo") y lanzado por primera vez en 2018. Nació de la necesidad de tener un framework para APIs en Python que fuera realmente rápido, fácil de usar y que aprovechara las características modernas del lenguaje.

Sebastián, después de trabajar con varios frameworks como Flask, Django y otros, identificó ciertos problemas comunes:

- Falta de validación automática de datos
- Documentación manual y tediosa
- Rendimiento limitado en comparación con frameworks de otros lenguajes
- Falta de soporte nativo para operaciones asíncronas

Para resolver estos problemas, creó FastAPI basándose en:

- **Starlette**: Para el manejo de solicitudes HTTP y operaciones asíncronas
- **Pydantic**: Para la validación, serialización y documentación de datos
- **Uvicorn/Hypercorn**: Como servidores ASGI de alto rendimiento
- **OpenAPI**: Para la documentación automática

## ¿Por qué FastAPI se volvió tan popular?

Desde su lanzamiento, FastAPI ha experimentado un crecimiento exponencial en popularidad por varias razones:

1. **Rendimiento excepcional**: Es uno de los frameworks Python más rápidos disponibles, comparable a Node.js y Go.
2. **Sintaxis intuitiva**: Aprovecha las anotaciones de tipo de Python 3.6+.
3. **Menos código, menos errores**: Reduce significativamente la cantidad de código necesario.
4. **Documentación automática**: Genera documentación interactiva sin esfuerzo adicional.
5. **Validación automática**: Valida los datos de entrada sin código adicional.
6. **Editor support**: Proporciona autocompletado y verificación de tipos en IDEs.

En 2023, FastAPI se convirtió en uno de los frameworks web de Python más populares, utilizado por empresas como Microsoft, Netflix, Uber y muchas startups.

## Fundamentos de FastAPI

### Conceptos Clave

#### 1. Instancia de la Aplicación

Todo comienza con la creación de una instancia de FastAPI:

```python
from fastapi import FastAPI

app = FastAPI()
```

Esta instancia es el punto central de tu aplicación, donde definirás rutas, middleware, eventos, etc.

#### 2. Rutas y Operaciones de Ruta

Las rutas se definen mediante decoradores que corresponden a métodos HTTP:

```python
@app.get("/items/")       # Obtener recursos
@app.post("/items/")      # Crear recursos
@app.put("/items/{id}")   # Actualizar recursos completos
@app.patch("/items/{id}") # Actualizar recursos parcialmente
@app.delete("/items/{id}") # Eliminar recursos
```

#### 3. Parámetros de Ruta

Puedes capturar valores de la URL usando parámetros de ruta:

```python
@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}
```

#### 4. Parámetros de Consulta

Los parámetros que se pasan en la URL después del signo de interrogación:

```python
@app.get("/items/")
def read_items(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}
```

#### 5. Modelos de Datos con Pydantic

FastAPI utiliza Pydantic para definir esquemas de datos:

```python
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

@app.post("/items/")
def create_item(item: Item):
    return item
```

### Características Avanzadas

#### 1. Operaciones Asíncronas

FastAPI soporta nativamente código asíncrono:

```python
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    item = await database.get_item(item_id)
    return item
```

#### 2. Dependencias

El sistema de inyección de dependencias permite reutilizar lógica:

```python
from fastapi import Depends

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/users/")
def read_users(db = Depends(get_db)):
    users = db.query(User).all()
    return users
```

#### 3. Seguridad y Autenticación

FastAPI facilita la implementación de seguridad:

```python
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/users/me")
async def read_users_me(token: str = Depends(oauth2_scheme)):
    return {"token": token}
```

## Arquitectura de FastAPI

### Capas Principales

1. **Capa ASGI**: Interfaz entre el servidor web y la aplicación
2. **Middleware**: Procesa solicitudes antes/después de llegar a las rutas
3. **Rutas**: Define los endpoints y sus manejadores
4. **Dependencias**: Proporciona inyección de dependencias
5. **Modelos Pydantic**: Valida y serializa datos

### Flujo de una Solicitud

1. El cliente envía una solicitud HTTP
2. El servidor ASGI (Uvicorn/Hypercorn) la recibe
3. La solicitud pasa por la cadena de middleware
4. FastAPI encuentra la ruta correspondiente
5. Se resuelven las dependencias
6. Se ejecuta la función de operación de ruta
7. La respuesta se serializa a JSON
8. La respuesta pasa por el middleware en orden inverso
9. El servidor ASGI envía la respuesta al cliente

## Comparación con Otros Frameworks

### FastAPI vs Flask

| Característica | FastAPI | Flask |
|---------------|---------|-------|
| Rendimiento | Alto (ASGI) | Moderado (WSGI) |
| Validación | Automática (Pydantic) | Manual o extensiones |
| Documentación | Automática (OpenAPI) | Manual o extensiones |
| Async/Await | Nativo | No soportado directamente |
| Tipado | Estático | Dinámico |
| Curva de aprendizaje | Moderada | Baja |

### FastAPI vs Django

| Característica | FastAPI | Django |
|---------------|---------|-------|
| Enfoque | API-first | Full-stack |
| Tamaño | Ligero | Completo |
| ORM | No incluido (usa SQLAlchemy) | Incluido |
| Admin | No incluido | Incluido |
| Rendimiento | Alto | Moderado |
| Async | Nativo | Parcial (reciente) |

## Mejores Prácticas

### Estructura del Proyecto

Para proyectos medianos a grandes, se recomienda esta estructura:

```
/myapp
  /app
    /api
      /endpoints
        user.py
        item.py
      /dependencies
        auth.py
        db.py
      router.py
    /core
      config.py
      security.py
    /db
      base.py
      models.py
      session.py
    /models
      user.py
      item.py
    /schemas
      user.py
      item.py
    main.py
```

### Consejos de Rendimiento

1. Usa operaciones asíncronas para E/S intensiva
2. Implementa caché cuando sea apropiado
3. Usa Pydantic para validación en lugar de validación manual
4. Configura correctamente el servidor ASGI (workers, límites)
5. Usa conexiones de base de datos asíncronas cuando sea posible

## Ejemplos Prácticos

### Ejemplo Básico: Hola Mundo

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "¡Hola, Mundo!"}
```

### Ejemplo CRUD Completo

```python
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# Modelo Pydantic
class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float

# Base de datos simulada
db = {}

@app.post("/items/", response_model=Item)
def create_item(item: Item):
    item_id = len(db) + 1
    db[item_id] = item.dict()
    return {"id": item_id, **item.dict()}

@app.get("/items/", response_model=List[Item])
def read_items(skip: int = 0, limit: int = 10):
    return list(db.values())[skip : skip + limit]

@app.get("/items/{item_id}", response_model=Item)
def read_item(item_id: int):
    if item_id not in db:
        raise HTTPException(status_code=404, detail="Item not found")
    return db[item_id]

@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, item: Item):
    if item_id not in db:
        raise HTTPException(status_code=404, detail="Item not found")
    db[item_id] = item.dict()
    return db[item_id]

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    if item_id not in db:
        raise HTTPException(status_code=404, detail="Item not found")
    del db[item_id]
    return {"message": "Item deleted"}
```

## Recursos de Aprendizaje

### Documentación Oficial
- [Documentación de FastAPI](https://fastapi.tiangolo.com/)
- [Tutorial Oficial](https://fastapi.tiangolo.com/tutorial/)
- [Guía Avanzada](https://fastapi.tiangolo.com/advanced/)

### Libros
- "FastAPI: Modern Python Web Development" por Sebastián Ramírez
- "Building Data Science Applications with FastAPI" por François Voron

### Cursos en Línea
- Udemy: "FastAPI - The Complete Course"
- TestDriven.io: "Developing and Testing an Asynchronous API with FastAPI"

### Comunidad
- [GitHub de FastAPI](https://github.com/tiangolo/fastapi)
- [Discord de FastAPI](https://discord.gg/VQjSZaeJmf)
- [Foro de Discusión](https://github.com/tiangolo/fastapi/discussions)

## Conclusión

FastAPI representa un avance significativo en el desarrollo de APIs con Python, combinando lo mejor de la tipificación estática, la validación automática y el rendimiento asíncrono. Su adopción continúa creciendo debido a su equilibrio entre facilidad de uso y potencia.

En un mundo donde las APIs son cada vez más importantes, FastAPI ofrece una solución moderna que satisface las necesidades de desarrolladores individuales y empresas por igual, permitiendo crear servicios web robustos, rápidos y bien documentados con menos código y menos errores.