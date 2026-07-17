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

## Versión 1.1 (Estabilización de Despliegue)

### Cambios
- Se solucionó el fallo de Healthcheck en Railway debido a problemas de bloqueo de base de datos.
- Se implementó un escudo protector (`try/except`) en `main.py` para evitar caídas si falla la conexión del webhook con Telegram.
- Se creó y ejecutó el script `fix_db.py` para liberar candados "fantasma" en la base de datos PostgreSQL de Railway (`AccessExclusiveLock`).
- Se removió la ejecución automática de migraciones (`alembic upgrade head`) del `Dockerfile` y `railway.toml` para permitir que el Healthcheck de Railway inicie `uvicorn` sin problemas de bloqueos simultáneos.
- Se limpió el comando de arranque de Railway para que utilice el comando encapsulado de Docker con variables de entorno correctamente formateadas (`$PORT`).

### Comandos Ejecutados y Salida
- `git add main.py; git commit -m "fix: atrapar error de webhook para evitar crash"; git push`
  - *Salida:* Commit 191d253. Inyectó blindaje para evitar que Uvicorn se cerrara por errores de Token en Telegram.
- `python fix_db.py` (Local)
  - *Salida:* "Connecting to database... Connected! Terminating all other connections to release locks... Other connections terminated. Fix applied successfully." Libera los bloqueos de base de datos que trababan a Alembic.
- `git commit -a -m "fix: remover startCommand de railway.toml para usar Dockerfile"`
  - *Salida:* Commit fce7cce. Eliminación del comando en Railway para que asuma el CMD de Docker y lea la variable `$PORT` con éxito, permitiendo así a Railway iniciar el contenedor.

## Versión 2.0 (Soporte Estructural de Categorías)

### Cambios
- Modificación estructural mayor para alinear el sistema al modelo real de Ligas y Categorías.
- Se agregó el modelo de base de datos `Category`.
- Se reasignaron las dependencias foráneas (`ForeignKey`) en las tablas `Team`, `Round` y `Match`, pasando de `tournament_id` a `category_id`.
- Se crearon flujos dinámicos en los handlers para que el bot solicite la creación de múltiples categorías al organizar un torneo.
- Se creó el teclado dinámico `get_categories_keyboard` para que los capitanes escojan en qué categoría desean inscribir a su equipo.
- Se actualizó el motor generador de brackets (`bracket_service`) para que elabore las llaves agrupando únicamente a los equipos por su categoría.

### Comandos Ejecutados y Salida
- `alembic revision --autogenerate -m "Add categories"`
  - *Salida:* `INFO [alembic.autogenerate.compare] Detected added table 'categories', Detected added column 'matches.category_id', ... Generating bd990dfa418d_add_categories.py ... done`
  - Generó los scripts de migración automáticos comparando el nuevo código con la base de datos PostgreSQL.
- `alembic upgrade head`
  - *Salida:* `INFO [alembic.runtime.migration] Running upgrade 804d96ded152 -> bd990dfa418d, Add categories`
  - Aplicó físicamente las alteraciones a las tablas de la base de datos sin pérdida de datos.
