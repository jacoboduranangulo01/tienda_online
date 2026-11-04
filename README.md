# Tienda Online — DevOps Práctica

**Autor:** Jacobo Durán Angulo

## Descripción
Aplicación Python de una tienda online: API REST con FastAPI (usuarios, productos y pedidos),
un cliente Python que consume la API por HTTP y un frontend web sencillo con `fetch`.
Los datos se guardan en memoria (se pierden al reiniciar). El proyecto está contenerizado con Docker.

## Estructura
```
.
├── Dockerfile
├── .dockerignore
├── requirements.txt         # dependencias con versiones fijadas
├── README.md
└── src/
    ├── main.py              # API FastAPI (punto de entrada)
    ├── schemas.py           # Esquemas Pydantic
    ├── cliente.py           # Cliente HTTP (requests)
    ├── models/              # Usuario, Producto, Pedido
    ├── services/            # TiendaService (lógica de negocio)
    └── frontend/index.html  # Frontend web
```

## Ejecución local (sin Docker)
```bash
python3 -m pip install -r requirements.txt
cd src
python3 -m uvicorn main:app --reload
```
Documentación interactiva: http://127.0.0.1:8000/docs

## Docker

### Requisitos
Docker Desktop instalado y en ejecución (`docker --version`).

### Construir la imagen
Desde la raíz del repositorio:
```bash
docker build -t tienda-online:1.0.0 -t tienda-online:latest .
```

### Ejecutar el contenedor
```bash
# En segundo plano, API en http://127.0.0.1:8000
docker run -d --name tienda -p 8000:8000 tienda-online:1.0.0

# En otro puerto del equipo (por ejemplo, 9000)
docker run -d --name tienda -p 9000:8000 tienda-online:1.0.0

# Cambiando el puerto interno con la variable PORT
docker run -d --name tienda -p 9000:9000 -e PORT=9000 tienda-online:1.0.0
```
Para pararlo y eliminarlo: `docker stop tienda && docker rm tienda`

### Variables de entorno
| Variable | Por defecto | Descripción |
|---|---|---|
| `PORT` | `8000` | Puerto en el que escucha la API dentro del contenedor. |
| `TIENDA_API_URL` | `http://127.0.0.1:8000` | Dirección de la API que usa `cliente.py`. |

No se guardan secretos en la imagen ni en el repositorio.

### Salida esperada y pasos de prueba
1. Comprobar que arrancó: `docker logs tienda` debe mostrar `Uvicorn running on http://0.0.0.0:8000`.
2. Raíz de la API: `curl http://127.0.0.1:8000/` debe devolver
   `{"mensaje":"API de la tienda online","documentacion":"/docs"}`.
3. Documentación: abrir http://127.0.0.1:8000/docs en el navegador.
4. Listar productos: `curl http://127.0.0.1:8000/productos` devuelve `[]` al inicio.
5. Ejecutar el cliente dentro del contenedor: `docker exec tienda python cliente.py`
   debe mostrar las respuestas `HTTP 201` (usuario, producto, pedido) y `HTTP 200` (listas e historial).
6. Comprobar que no corre como root: `docker exec tienda whoami` debe devolver `appuser`.

### Publicar y descargar la imagen (Docker Hub)
```bash
docker login
docker tag tienda-online:1.0.0 jacoboduranangulo01/tienda-online:1.0.0
docker tag tienda-online:1.0.0 jacoboduranangulo01/tienda-online:latest
docker push jacoboduranangulo01/tienda-online:1.0.0
docker push jacoboduranangulo01/tienda-online:latest
```
Descargar y ejecutar desde el registry:
```bash
docker pull jacoboduranangulo01/tienda-online:1.0.0
docker run -d --name tienda -p 8000:8000 jacoboduranangulo01/tienda-online:1.0.0
```

## Flujo de trabajo con Git
Rama `main` protegida; el trabajo se hace en ramas `feature/*` con commits pequeños
y se integra mediante Pull Request.
