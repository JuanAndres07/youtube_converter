# syntax=docker/dockerfile:1

FROM python:3.12-slim

# Ajustes Python y pip
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Dependencias del sistema (ffmpeg + compilar wheels si hace falta)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    build-essential \
 && rm -rf /var/lib/apt/lists/*

# Directorio de trabajo
WORKDIR /app

# Crear usuario no-root (mejor práctica)
RUN useradd -ms /bin/bash appuser

# Instalar deps de Python primero para aprovechar cache de Docker
COPY requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copiar el resto del código
COPY . .

# Normalizar finales de línea y hacer ejecutable el entrypoint (evita error en Windows)
RUN sed -i 's/\r$//' entrypoint.sh && chmod +x entrypoint.sh

# Permisos al usuario appuser
RUN chown -R appuser:appuser /app
USER appuser

# Render inyecta $PORT; exponemos 8000 para uso local
EXPOSE 8000

# Script que corre antes del servidor
ENTRYPOINT ["bash", "entrypoint.sh"]

# Comando por defecto: usa $PORT si existe, 8000 si no
CMD gunicorn core.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers 2 --timeout 180
