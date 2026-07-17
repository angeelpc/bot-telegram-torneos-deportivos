FROM python:3.12-slim

WORKDIR /app

# Instalar dependencias del sistema útiles para psycopg/asyncpg si fueran necesarias
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Instalar dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY . .

# Comando para aplicar migraciones y luego arrancar la aplicación
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port $PORT"]
