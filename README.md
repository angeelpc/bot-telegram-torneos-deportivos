# Bot de Telegram para Torneos Deportivos

Este es un bot de Telegram diseñado para organizar torneos deportivos de eliminación directa. Construido con Python, FastAPI, aiogram 3, PostgreSQL, SQLAlchemy y Alembic.

## Requisitos Previos

- Python 3.12+
- PostgreSQL
- Una cuenta de Telegram y un bot creado con [@BotFather](https://t.me/BotFather)

## Configuración Local

1. Clona este repositorio.
2. Crea un entorno virtual: `python -m venv venv` y actívalo (`venv\Scripts\activate` en Windows).
3. Instala las dependencias: `pip install -r requirements.txt`.
4. Copia el archivo `.env.example` a `.env` y rellena las variables de entorno:
   - `TELEGRAM_BOT_TOKEN`: Obtenido de BotFather.
   - `DATABASE_URL`: URL de conexión a tu base de datos local PostgreSQL (ej. `postgresql+asyncpg://user:pass@localhost/torneos`).
   - `APP_BASE_URL`: URL base para el webhook (si usas ngrok localmente: `https://tu-url.ngrok.app`).
   - `TELEGRAM_WEBHOOK_SECRET`: Un string aleatorio para proteger el webhook.
5. Ejecuta las migraciones de la base de datos para crear las tablas:
   ```bash
   alembic upgrade head
   ```
6. Inicia el servidor:
   ```bash
   uvicorn main:app --reload
   ```

## Creación del Bot con BotFather

1. Abre Telegram y busca a `@BotFather`.
2. Envía el comando `/newbot`.
3. Sigue las instrucciones para asignarle un nombre y un username.
4. Copia el **Token HTTP API** y colócalo en tu `.env`.

## Configuración de PostgreSQL

1. Instala PostgreSQL en tu sistema.
2. Abre psql o PgAdmin y crea una base de datos:
   ```sql
   CREATE DATABASE torneos;
   ```
3. Asegúrate de que las credenciales coincidan con la `DATABASE_URL` en tu `.env`.

## Despliegue en Railway

1. Crea un proyecto en [Railway](https://railway.app/).
2. Añade un servicio de base de datos PostgreSQL.
3. Conecta tu repositorio de GitHub al proyecto de Railway.
4. Railway detectará automáticamente el archivo `railway.toml` y el `Dockerfile`.
5. En los "Variables" del servicio de tu aplicación, configura:
   - `TELEGRAM_BOT_TOKEN`
   - `TELEGRAM_WEBHOOK_SECRET`
   - `APP_BASE_URL` (Usa el dominio público generado por Railway)
   - `DATABASE_URL` (Proporcionada por el servicio de PostgreSQL de Railway, asegúrate de cambiar `postgresql://` por `postgresql+asyncpg://`)
6. El despliegue ejecutará las migraciones y configurará el webhook de Telegram al iniciar.
