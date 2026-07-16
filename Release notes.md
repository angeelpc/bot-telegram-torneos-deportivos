# Release Notes

## Versión 1.0 (MVP)

### Cambios
- Inicialización del proyecto MVP del bot de Telegram para organizar torneos deportivos.
- Estructura de carpetas creada según el plan arquitectónico.
- Configuración de FastAPI, aiogram 3, PostgreSQL, SQLAlchemy y Alembic.
- Creación de archivos de infraestructura (`Dockerfile`, `railway.toml`, `.env.example`).
- Implementación de la lógica de bracket, bye y avance.

### Comandos Ejecutados
*NOTA: Se incluyen los comandos clave que configuran el proyecto inicial.*
- `alembic init db/migrations`: Crea el entorno de migraciones.
- `pip install -r requirements.txt`: Instalación de dependencias.
