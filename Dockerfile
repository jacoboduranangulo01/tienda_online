# 1. Imagen base ligera de Python
FROM python:3.12-slim

# Sin .pyc y con logs en tiempo real
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000

# Usuario sin privilegios para ejecutar la app (no root)
RUN useradd --create-home --shell /usr/sbin/nologin appuser

WORKDIR /app

# 2. Dependencias primero (aprovecha la caché de capas)
COPY requirements.txt .
# 3. Instalación sin caché para reducir el tamaño de la imagen
RUN pip install --no-cache-dir -r requirements.txt

# 4. Código fuente, con permisos para el usuario appuser
COPY --chown=appuser:appuser src/ ./src/

# 5. Ejecutar como appuser desde la carpeta del código
USER appuser
WORKDIR /app/src

EXPOSE 8000

# 6. Comando de inicio (el puerto se puede cambiar con la variable PORT)
CMD ["sh", "-c", "exec uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]
