# ---- Base image
FROM python:3.12-slim

# ---- System setup
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# (opcional) instala curl para healthcheck
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*

# Crea usuario no root
RUN useradd -m appuser
WORKDIR /app

# ---- Dependencias
# Copiamos solo requirements primero para aprovechar cache
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# ---- Código
COPY . /app
RUN chown -R appuser:appuser /app
USER appuser

# ---- Expose (informativo)
EXPOSE 8000

# ---- Healthcheck (asumiendo endpoint /health_check)
HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
  CMD curl -fsS http://127.0.0.1:${PORT:-8000}/health_check || exit 1

# ---- Start
# Render inyecta $PORT. Si no existe, usa 8000.
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]
