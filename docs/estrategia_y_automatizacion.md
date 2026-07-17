# Estrategia Comercial y Automatización

## 1. Modelo de Negocio y Ventas
Para asegurar la viabilidad económica y el crecimiento continuo de la plataforma, se proponen los siguientes modelos de monetización (estrategia de precios):

* **Suscripción SaaS para Organizadores (Liga/Torneo):** Cobrar una tarifa mensual o anual a los organizadores por el uso de la plataforma. Se pueden ofrecer niveles (Tiers) basados en el volumen, por ejemplo:
    * *Tier Básico:* Gratuito o de muy bajo costo. Límite de 1 torneo y hasta 8 equipos.
    * *Tier Pro:* Precio intermedio. Torneos ilimitados, múltiples categorías, estadísticas avanzadas.
    * *Tier Enterprise:* Para ligas muy grandes, integrando dominios personalizados, múltiples administradores y soporte prioritario.
* **Cobro por Equipo o Categoría:** Cobrar una pequeña comisión o tarifa fija por cada equipo inscrito o por categoría creada, asegurando que el precio se escale con el tamaño del torneo.
* **Freemium con Publicidad:** Ofrecer la gestión del torneo gratuitamente para torneos pequeños, pero con anuncios en el sitio web público o en los mensajes del bot. Se puede cobrar por remover los anuncios.
* **Patrocinios:** Permitir que marcas patrocinen ligas completas o categorías específicas, monetizando espacios destacados dentro del bracket.

## 2. Automatizaciones Viables
Para reducir drásticamente la carga operativa de los organizadores y enriquecer la experiencia de los jugadores, se contemplan las siguientes automatizaciones:

* **Recordatorios de Partidos (24h Match Reminders):** El bot enviará automáticamente un mensaje a los capitanes o equipos involucrados 24 horas antes del inicio de su partido.
* **Progresión Automática del Bracket (Automatic Bracket Progression):** Al reportarse el resultado (por los capitanes y aprobado, o por el administrador), el equipo ganador avanzará de forma automática a la siguiente ronda, actualizando las llaves en la base de datos de manera inmediata.
* **Gestión Disciplinaria (Automatic Suspensions):** Si se registran tarjetas rojas o acumulación de tarjetas amarillas durante el reporte de resultados, el sistema suspenderá automáticamente al jugador para el siguiente partido, alertando al capitán.
* **Resolución de Empates en Grupos (Group Stage Tiebreakers):** En fases de grupos, la tabla de posiciones se ordenará automáticamente según las reglas predefinidas (diferencia de goles, goles a favor, resultados entre sí).
* **Alerta de Resultados Faltantes:** Automatización para notificar a los capitanes/árbitros de partidos finalizados sin un marcador reportado.

## 3. Viabilidad Web (Arquitectura Headless)
Actualmente, el sistema opera a través del bot de Telegram apoyado en un backend robusto. La exposición de estos datos en una plataforma pública es completamente viable utilizando una arquitectura Headless.

* **Separación de Responsabilidades (Headless):** 
    * El bot de Telegram seguirá sirviendo como el principal panel de control ("Backoffice") para acciones de administración y reporte de resultados (junto con la API).
    * El backend (FastAPI/Postgres) actuará como un proveedor de datos agnóstico (Headless CMS/Backend).
* **Frontend Moderno:** Se desarrollará un frontend utilizando un framework moderno (ej. **React o Next.js**) que consumirá los endpoints REST de nuestra API. Next.js permitirá ventajas como Server-Side Rendering (SSR) o Static Site Generation (SSG) para mostrar el bracket y los resultados en tiempo real, lo que mejorará dramáticamente el SEO de las páginas de torneos.
* **Despliegue Independiente:** El frontend se desplegará de forma independiente (por ejemplo, en Vercel o Netlify), asegurando que un alto tráfico de visitas a los brackets públicos no comprometa la capacidad del backend/bot para procesar los comandos de los usuarios.
* **Consolidación de Datos:** Toda la información (equipos, resultados, rondas) vendrá de la misma fuente de verdad (la base de datos Postgres), asegurando que el sitio web siempre muestre la misma información actualizada al momento mediante el bot.
