# Importamos las clases y módulos necesarios
from fastapi import FastAPI, HTTPException, status, Path, Query, Body, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime

# Creamos una instancia de FastAPI
app = FastAPI(
    title="API de Ejemplo con Todos los Métodos HTTP",
    description="Ejemplo que muestra cómo implementar GET, POST, PUT, PATCH y DELETE en FastAPI",
    version="1.0.0"
)

# =========================================================
# MODELOS DE DATOS (SCHEMAS)
# =========================================================

# Modelo base para productos (campos comunes)
class ProductoBase(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=50, description="Nombre del producto")
    descripcion: Optional[str] = Field(None, max_length=200, description="Descripción detallada del producto")
    precio: float = Field(..., gt=0, description="Precio del producto en USD")
    disponible: bool = Field(True, description="Indica si el producto está disponible")
    categorias: List[str] = Field(default=[], description="Lista de categorías a las que pertenece el producto")

# Modelo para crear un nuevo producto (sin ID)
class ProductoCreate(ProductoBase):
    pass

# Modelo para actualizar un producto completamente
class ProductoUpdate(ProductoBase):
    pass

# Modelo para actualizar un producto parcialmente
class ProductoPatch(BaseModel):
    nombre: Optional[str] = Field(None, min_length=3, max_length=50)
    descripcion: Optional[str] = Field(None, max_length=200)
    precio: Optional[float] = Field(None, gt=0)
    disponible: Optional[bool] = None
    categorias: Optional[List[str]] = None

# Modelo para respuesta (incluye ID)
class Producto(ProductoBase):
    id: int
    fecha_creacion: datetime
    fecha_actualizacion: Optional[datetime] = None
    
    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "nombre": "Smartphone XYZ",
                "descripcion": "Un smartphone de última generación",
                "precio": 599.99,
                "disponible": True,
                "categorias": ["Electrónica", "Móviles"],
                "fecha_creacion": "2025-04-12T11:30:00",
                "fecha_actualizacion": "2025-04-12T11:35:00"
            }
        }

# =========================================================
# BASE DE DATOS SIMULADA
# =========================================================

# Base de datos en memoria para almacenar productos
db_productos = {
    1: {
        "id": 1,
        "nombre": "Laptop Pro",
        "descripcion": "Laptop de alta gama para profesionales",
        "precio": 1299.99,
        "disponible": True,
        "categorias": ["Electrónica", "Computadoras"],
        "fecha_creacion": datetime.now(),
        "fecha_actualizacion": None
    },
    2: {
        "id": 2,
        "nombre": "Smartphone Galaxy",
        "descripcion": "Smartphone con cámara de alta resolución",
        "precio": 899.99,
        "disponible": True,
        "categorias": ["Electrónica", "Móviles"],
        "fecha_creacion": datetime.now(),
        "fecha_actualizacion": None
    },
    3: {
        "id": 3,
        "nombre": "Auriculares Noise-Cancelling",
        "descripcion": "Auriculares con cancelación de ruido",
        "precio": 249.99,
        "disponible": False,
        "categorias": ["Electrónica", "Audio"],
        "fecha_creacion": datetime.now(),
        "fecha_actualizacion": None
    }
}

# Variable para simular el auto-incremento de IDs
siguiente_id = 4

# =========================================================
# DEPENDENCIAS
# =========================================================

# Función de dependencia para verificar si un producto existe
def verificar_producto_existe(producto_id: int = Path(..., gt=0)):
    if producto_id not in db_productos:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El producto con ID {producto_id} no existe"
        )
    return producto_id

# =========================================================
# RUTAS (ENDPOINTS)
# =========================================================

# Ruta raíz - GET
@app.get("/", tags=["Inicio"])
def read_root():
    """Endpoint principal que devuelve un mensaje de bienvenida."""
    return {"mensaje": "Bienvenido a la API de ejemplo con todos los métodos HTTP"}

# =========================================================
# OPERACIONES CRUD PARA PRODUCTOS
# =========================================================

# 1. GET - Obtener todos los productos (READ - Colection)
@app.get("/productos", 
         response_model=List[Producto], 
         status_code=status.HTTP_200_OK,
         tags=["Productos"],
         summary="Obtener lista de productos")
def get_productos(
    skip: int = Query(0, ge=0, description="Número de registros para saltar"),
    limit: int = Query(10, ge=1, le=100, description="Número máximo de registros a devolver"),
    disponible: Optional[bool] = Query(None, description="Filtrar por disponibilidad")
):
    """Obtiene una lista de productos con opciones de paginación y filtrado.
    
    - **skip**: Número de productos a saltar (paginación)
    - **limit**: Número máximo de productos a devolver
    - **disponible**: Filtrar productos por disponibilidad
    """
    # Convertimos los valores del diccionario a una lista
    productos = list(db_productos.values())
    
    # Aplicamos filtro por disponibilidad si se especifica
    if disponible is not None:
        productos = [p for p in productos if p["disponible"] == disponible]
    
    # Aplicamos paginación
    return productos[skip:skip + limit]

# 2. GET - Obtener un producto por ID (READ - Individual)
@app.get("/productos/{producto_id}", 
         response_model=Producto,
         status_code=status.HTTP_200_OK,
         tags=["Productos"],
         summary="Obtener un producto por ID")
def get_producto(producto_id: int = Depends(verificar_producto_existe)):
    """Obtiene un producto específico por su ID.
    
    - **producto_id**: ID del producto a obtener
    """
    return db_productos[producto_id]

# 3. POST - Crear un nuevo producto (CREATE)
@app.post("/productos", 
          response_model=Producto, 
          status_code=status.HTTP_201_CREATED,
          tags=["Productos"],
          summary="Crear un nuevo producto")
def create_producto(producto: ProductoCreate = Body(...)):
    """Crea un nuevo producto en la base de datos.
    
    - **producto**: Datos del producto a crear
    """
    global siguiente_id
    
    # Creamos un nuevo producto con ID auto-incrementado
    nuevo_producto = producto.dict()
    nuevo_producto["id"] = siguiente_id
    nuevo_producto["fecha_creacion"] = datetime.now()
    nuevo_producto["fecha_actualizacion"] = None
    
    # Guardamos en la base de datos
    db_productos[siguiente_id] = nuevo_producto
    siguiente_id += 1
    
    return nuevo_producto

# 4. PUT - Actualizar un producto completo (UPDATE)
@app.put("/productos/{producto_id}", 
         response_model=Producto,
         status_code=status.HTTP_200_OK,
         tags=["Productos"],
         summary="Actualizar un producto completamente")
def update_producto(
    producto_update: ProductoUpdate,
    producto_id: int = Depends(verificar_producto_existe)
):
    """Actualiza completamente un producto existente.
    
    - **producto_id**: ID del producto a actualizar
    - **producto_update**: Nuevos datos completos del producto
    """
    # Obtenemos el producto existente
    producto_existente = db_productos[producto_id]
    
    # Actualizamos todos los campos
    producto_actualizado = producto_update.dict()
    producto_actualizado["id"] = producto_id
    producto_actualizado["fecha_creacion"] = producto_existente["fecha_creacion"]
    producto_actualizado["fecha_actualizacion"] = datetime.now()
    
    # Guardamos en la base de datos
    db_productos[producto_id] = producto_actualizado
    
    return producto_actualizado

# 5. PATCH - Actualizar parcialmente un producto (UPDATE PARTIAL)
@app.patch("/productos/{producto_id}", 
           response_model=Producto,
           status_code=status.HTTP_200_OK,
           tags=["Productos"],
           summary="Actualizar un producto parcialmente")
def patch_producto(
    producto_patch: ProductoPatch,
    producto_id: int = Depends(verificar_producto_existe)
):
    """Actualiza parcialmente un producto existente.
    
    - **producto_id**: ID del producto a actualizar parcialmente
    - **producto_patch**: Campos a actualizar del producto
    """
    # Obtenemos el producto existente
    producto_existente = db_productos[producto_id]
    
    # Convertimos a diccionario para facilitar la actualización
    producto_actualizado = dict(producto_existente)
    
    # Actualizamos solo los campos que vienen en la solicitud
    update_data = producto_patch.dict(exclude_unset=True)
    for campo, valor in update_data.items():
        producto_actualizado[campo] = valor
    
    # Actualizamos la fecha de actualización
    producto_actualizado["fecha_actualizacion"] = datetime.now()
    
    # Guardamos en la base de datos
    db_productos[producto_id] = producto_actualizado
    
    return producto_actualizado

# 6. DELETE - Eliminar un producto (DELETE)
@app.delete("/productos/{producto_id}", 
            status_code=status.HTTP_204_NO_CONTENT,
            tags=["Productos"],
            summary="Eliminar un producto")
def delete_producto(producto_id: int = Depends(verificar_producto_existe)):
    """Elimina un producto de la base de datos.
    
    - **producto_id**: ID del producto a eliminar
    """
    # Eliminamos el producto de la base de datos
    del db_productos[producto_id]
    
    # Retornamos 204 No Content (sin cuerpo de respuesta)
    return None

# 7. GET - Buscar productos por nombre (SEARCH)
@app.get("/productos/buscar/", 
         response_model=List[Producto],
         tags=["Productos"],
         summary="Buscar productos por nombre")
def search_productos(q: str = Query(..., min_length=2, description="Término de búsqueda")):
    """Busca productos que contengan el término de búsqueda en su nombre.
    
    - **q**: Término de búsqueda (mínimo 2 caracteres)
    """
    resultados = [p for p in db_productos.values() if q.lower() in p["nombre"].lower()]
    return resultados