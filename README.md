# Tienda Online — DevOps Práctica

**Autor:** JAcobo Durán Angulo

## Descripción
Aplicación Python de una tienda online: API REST con FastAPI (usuarios, productos y pedidos),
un cliente Python que consume la API por HTTP y un frontend web sencillo con `fetch`.
Los datos se guardan en memoria. Este repositorio se usa para practicar control de versiones
con Git/GitHub y, en las siguientes prácticas, contenerización con Docker.

## Estructura
```
.
├── main.py              # API FastAPI
├── schemas.py           # Esquemas Pydantic
├── cliente.py           # Cliente HTTP (requests)
├── models/              # Usuario, Producto, Pedido
├── services/            # TiendaService (lógica de negocio)
├── frontend/index.html  # Frontend web
└── requirements.txt
```

## 1. Preparación en Visual Studio Code
1. Descomprime el ZIP y abre la carpeta del repositorio en Visual Studio Code.
2. Abre Terminal > Nueva terminal.
3. Instala las dependencias:
   `python -m pip install -r requirements.txt`
   En algunos equipos usa `python3 -m pip install -r requirements.txt`.

## 2. Iniciar la API en el mismo equipo
Desde la carpeta que contiene `main.py`, ejecuta:
`python -m uvicorn main:app --reload`

Abre `http://127.0.0.1:8000/docs`.

## 3. Probar el cliente Python
Deja la API ejecutándose. Abre una segunda terminal en la misma carpeta y ejecuta:
`python cliente.py`

El cliente crea un cliente de prueba y un producto, consulta las listas, crea un pedido y consulta su historial. Los datos se guardan en memoria y se pierden al reiniciar el servidor. Cada ejecución del cliente crea nuevos registros.

Puedes cambiar la dirección mediante la variable de entorno `TIENDA_API_URL`; por defecto es `http://127.0.0.1:8000`.

## 4. Probar el frontend
Con la API activa, abre `frontend/index.html` en el navegador. En “Conexión con la API” deja `http://127.0.0.1:8000` y pulsa “Actualizar datos”.
El frontend permite ver y crear productos, ver y crear clientes, crear pedidos y consultar el historial de pedidos. Los errores HTTP se muestran en pantalla.

## 5. Prueba entre dos ordenadores en la misma red
En el equipo que ejecuta la API:
1. Consulta su IP local:
   - Windows: `ipconfig`
   - macOS/Linux: `ifconfig` o `ip addr`
2. Inicia el servidor escuchando en la red:
   `python -m uvicorn main:app --host 0.0.0.0 --port 8000`
3. Si el firewall pregunta, permite conexiones privadas/locales al puerto 8000.

En el segundo equipo, sustituye la dirección base por la IP del equipo servidor, por ejemplo:
`http://192.168.1.34:8000`
Prueba esa dirección en el campo de conexión del frontend y abre `http://192.168.1.34:8000/docs` en el navegador del segundo equipo.

Para ejecutar `cliente.py` en el segundo equipo, establece `TIENDA_API_URL` con la IP del servidor:
- Windows PowerShell: `$env:TIENDA_API_URL="http://192.168.1.34:8000"`
- macOS/Linux: `export TIENDA_API_URL="http://192.168.1.34:8000"`
Luego ejecuta `python cliente.py`.

## Endpoints de la API
- `POST /usuarios`, `GET /usuarios`, `GET /usuarios/{usuario_id}`
- `POST /productos`, `GET /productos`, `GET /productos/{producto_id}`, `DELETE /productos/{producto_id}`
- `POST /pedidos`, `GET /usuarios/{cliente_id}/pedidos`

## Notas
- La aplicación almacena datos en memoria, no en una base de datos.
- El frontend usa `fetch` para peticiones HTTP; el cliente Python usa `requests`.
- Para uso real fuera de un entorno académico, habría que restringir CORS y añadir persistencia y autenticación.

## Docker
```bash
docker build -t tienda-online .
docker run --rm -p 8000:8000 tienda-online
```
La API queda disponible en `http://127.0.0.1:8000/docs`.
