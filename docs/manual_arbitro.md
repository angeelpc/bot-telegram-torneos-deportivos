# Manual del Árbitro (Visión a Futuro)

Este manual es una proyección de las funciones que tendrán los árbitros dentro del Bot de Telegram en futuras versiones. Su propósito es facilitar el reporte de resultados directamente desde la cancha.

## 1. Asignación y Autenticación
Los árbitros serán registrados por el administrador de la liga y se vincularán a su cuenta de Telegram.
- **Notificaciones de Asignación:** El árbitro recibirá un mensaje con la hora, lugar y equipos del partido que debe pitar.
- **Autenticación:** El sistema reconocerá al usuario como "Árbitro Oficial" permitiéndole acceso a comandos especiales.

## 2. Reporte de Resultados
Al finalizar un partido, el árbitro podrá ingresar el marcador de manera rápida y sencilla.
- **Comando Futuro:** `/reportar_resultado`
- **Flujo Esperado:**
  1. El bot mostrará los partidos asignados al árbitro en ese día.
  2. El árbitro seleccionará el partido recién finalizado.
  3. El bot solicitará los goles/puntos del Equipo A y luego los del Equipo B.
  4. El sistema pedirá una confirmación final antes de registrar el resultado en la base de datos y avanzar al ganador en el bracket.

## 3. Gestión de Tarjetas y Sanciones
Además de los goles, el árbitro podrá registrar incidencias.
- **Registro Rápido:** Mediante botones interactivos, el árbitro podrá indicar si hubo tarjetas amarillas o rojas para ciertos jugadores (si el sistema maneja roster de jugadores).
- **Reporte de Incidencias:** Existirá la opción de enviar un breve reporte de texto o nota de voz al bot detallando cualquier comportamiento antideportivo, el cual será reenviado al Administrador de Liga.

## 4. Transparencia y Notificaciones
Una vez que el árbitro confirma el resultado:
- El bot enviará automáticamente una notificación a los capitanes de ambos equipos informando el resultado oficial del partido y qué equipo avanza a la siguiente ronda.
- Si hay una disputa, los capitanes tendrán un lapso de tiempo definido para reportarlo al administrador antes de que el resultado sea inamovible.
