# Manual del Administrador de Liga

Este manual detalla los pasos y comandos necesarios para gestionar un torneo dentro de la plataforma del Bot de Telegram.

## 1. Crear un Torneo
Para iniciar un nuevo torneo, el administrador debe interactuar con el bot mediante el comando `/crear_torneo`.
- **Paso 1:** Ejecutar `/crear_torneo` en el chat con el bot.
- **Paso 2:** Proporcionar el nombre del torneo (ej: "Torneo de Verano 2026").
- **Paso 3:** Definir el deporte y las reglas básicas cuando el bot lo solicite.

## 2. Definir Categorías
Una vez creado el torneo, el bot pedirá definir las categorías disponibles.
- **Paso 1:** Seleccionar "Agregar Categoría".
- **Paso 2:** Ingresar el nombre de la categoría (ej: "Primera División", "Femenil Libre").
- **Paso 3:** Repetir el proceso hasta completar todas las categorías y presionar "Finalizar Categorías".

## 3. Cierre de Inscripciones
Cuando el administrador decide que no se admitirán más equipos, se debe cerrar la inscripción.
- **Paso 1:** Usar el comando `/cerrar_inscripcion`.
- **Paso 2:** Seleccionar el torneo activo en el menú interactivo.
- **Paso 3:** Confirmar el cierre. A partir de este momento, los enlaces de invitación (deep links) dejarán de funcionar para nuevos equipos.

## 4. Generación de Brackets (Llaves)
Con las inscripciones cerradas, se pueden generar los enfrentamientos.
- **Paso 1:** Utilizar el comando `/generar_bracket`.
- **Paso 2:** El bot organizará automáticamente a los equipos inscritos agrupándolos por su respectiva categoría.
- **Paso 3:** Si la cantidad de equipos en una categoría no es potencia de 2, el bot asignará "Byes" (pases directos) a los equipos correspondientes de forma aleatoria o según el seed, si aplica.

## 5. Gestión de Partidos (Matches)
El administrador también puede supervisar el avance del torneo.
- **Paso 1:** Usar `/ver_partidos` para listar los enfrentamientos actuales.
- **Paso 2:** En caso de emergencia, el administrador puede intervenir un partido para forzar un resultado si un árbitro no está disponible.
- **Paso 3:** Al finalizar una ronda completa, el bot avanzará automáticamente a los ganadores a la siguiente ronda (o el administrador puede confirmarlo manualmente si está configurado así).
