## Endpoints Disponibles

### GET /

- **URL:** `http://127.0.0.1:8000/`
- **Descripción:** Endpoint principal que devuelve un mensaje de bienvenida.
- **Tags:** Inicio

---

### GET /productos

- **URL:** `http://127.0.0.1:8000/productos`
- **Query Params:**
  - `skip` (int, opcional): Número de registros para saltar (default: 0).
  - `limit` (int, opcional): Número máximo de registros a devolver (default: 10, max: 100).
  - `disponible` (bool, opcional): Filtrar por disponibilidad.
- **Descripción:** Obtiene una lista paginada de productos con opción de filtrado.
- **Tags:** Productos

---

### GET /productos/{producto_id}

- **URL:** `http://127.0.0.1:8000/productos/1` (ejemplo para ID 1)
- **Descripción:** Obtiene un producto específico por su ID.
- **Tags:** Productos

---

### POST /productos

- **URL:** `http://127.0.0.1:8000/productos`
- **Body:** Datos del producto en formato JSON (según `ProductoCreate`).
- **Descripción:** Crea un nuevo producto en la base de datos.
- **Tags:** Productos

---

### PUT /productos/{producto_id}

- **URL:** `http://127.0.0.1:8000/productos/1` (ejemplo para ID 1)
- **Body:** Datos completos del producto en formato JSON (según `ProductoUpdate`).
- **Descripción:** Actualiza completamente un producto existente.
- **Tags:** Productos

---

### PATCH /productos/{producto_id}

- **URL:** `http://127.0.0.1:8000/productos/1` (ejemplo para ID 1)
- **Body:** Campos parciales del producto en formato JSON (según `ProductoPatch`).
- **Descripción:** Actualiza parcialmente un producto existente.
- **Tags:** Productos

---

### DELETE /productos/{producto_id}

- **URL:** `http://127.0.0.1:8000/productos/1` (ejemplo para ID 1)
- **Descripción:** Elimina un producto de la base de datos.
- **Tags:** Productos

---

### GET /productos/buscar/

- **URL:** `http://127.0.0.1:8000/productos/buscar/?q=smartphone` (ejemplo para buscar "smartphone")
- **Query Params:**
  - `q` (str, requerido): Término de búsqueda (mínimo 2 caracteres).
- **Descripción:** Busca productos que contengan el término en su nombre.
- **Tags:** Productos

