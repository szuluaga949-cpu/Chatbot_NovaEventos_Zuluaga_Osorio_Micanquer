# 🧪 Matriz de 25 Pruebas · Proyecto NovaEventos (Entrega Final)

> **Proyecto:** NovaEventos — Chatbot de Reservas para Centro de Convenciones  
> **Stack:** Telegram Bot + FastAPI + SQLite  
> **Fecha de ejecución:** 21 de noviembre de 2026  
> **Responsable de pruebas:** Equipo NovaEventos  
> **Versión del sistema:** 1.0 — Entrega Final

---

## 📑 Documentos Relacionados

| Documento | Enlace |
|-----------|--------|
| Bitácora Consolidada | [Bitacora_Consolidada.md](./Bitacora_Consolidada.md) |
| README del Proyecto | [README.md](../README.md) |
| Carpeta de Evidencias | [`../evidencias/`](../evidencias/) |

---

## 🏢 Espacios del Centro de Convenciones

| Código | Nombre | Espacio | Duración | Capacidad Máx. |
|--------|--------|---------|----------|----------------|
| EVT-CORP | Conferencia Corporativa | Auditorio Nova | 4 h | 100 personas |
| EVT-BODA | Recepción de Boda | Salón Imperial | 5 h | 200 personas |
| EVT-CUMP | Celebración de Cumpleaños | Salón Social | 4 h | 80 personas |
| EVT-WORK | Taller Ejecutivo | Sala Innovación | 2 h | 30 personas |

> **Horario de operación:** 08:00 – 22:00 · **Formato de códigos:** NOVA-XXXX

---

## 📊 Tabla Resumen de las 25 Pruebas

| # | Caso | Grupo | Cumplimiento |
|---|------|-------|:------------:|
| T01 | Consulta general de servicios/espacios | 1 · Conversaciones normales | ✅ |
| T02 | Consulta de precio de un servicio | 1 · Conversaciones normales | ✅ |
| T03 | Reserva completa en un solo mensaje | 1 · Conversaciones normales | ✅ |
| T04 | Reserva multi-turno (4 pasos) | 1 · Conversaciones normales | ✅ |
| T05 | Saludo y navegación del menú | 1 · Conversaciones normales | ✅ |
| T06 | Consulta de disponibilidad de horario específico | 1 · Conversaciones normales | ✅ |
| T07 | Mensaje sin servicio identificable | 2 · Preguntas ambiguas o incompletas | ✅ |
| T08 | Fecha sin formato correcto | 2 · Preguntas ambiguas o incompletas | ✅ |
| T09 | Número de asistentes no especificado | 2 · Preguntas ambiguas o incompletas | ✅ |
| T10 | Mensaje con múltiples intenciones | 2 · Preguntas ambiguas o incompletas | ✅ |
| T11 | Dos cuentas con solicitudes independientes | 3 · Contexto, memoria y estado | ✅ |
| T12 | Reinicio de sesión (/reiniciar) | 3 · Contexto, memoria y estado | ✅ |
| T13 | Cambio de dato en medio de la conversación | 3 · Contexto, memoria y estado | ✅ |
| T14 | Confirmación repetida / botón antiguo | 3 · Contexto, memoria y estado | ✅ |
| T15 | Pregunta no relacionada con el dominio | 4 · Fuera del dominio | ✅ |
| T16 | Intento de inyección (código/SQL) | 4 · Fuera del dominio | ✅ |
| T17 | Mensaje vacío o solo emojis | 4 · Fuera del dominio | ✅ |
| T18 | Creación exitosa con registro en SQLite | 5 · Operaciones de reserva | ✅ |
| T19 | Consulta de reserva propia (/consultar) | 5 · Operaciones de reserva | ✅ |
| T20 | Cancelación de reserva propia (/cancelar) | 5 · Operaciones de reserva | ✅ |
| T21 | Rechazo de cruce de horario | 5 · Operaciones de reserva | ✅ |
| T22 | Rechazo de acceso a reserva ajena | 5 · Operaciones de reserva | ✅ |
| T23 | Horario fuera del rango de atención | 6 · Errores y situaciones límite | ✅ |
| T24 | Capacidad máxima excedida | 6 · Errores y situaciones límite | ✅ |
| T25 | Reserva con código inexistente | 6 · Errores y situaciones límite | ✅ |

> **Resultado global: 25 / 25 pruebas aprobadas ✅**

---

## 📂 Distribución por Grupo

| Grupo | Descripción | Cantidad | Pruebas |
|-------|-------------|:--------:|---------|
| 1 | Conversaciones normales | 6 | T01 – T06 |
| 2 | Preguntas ambiguas o incompletas | 4 | T07 – T10 |
| 3 | Contexto, memoria y estado | 4 | T11 – T14 |
| 4 | Fuera del dominio | 3 | T15 – T17 |
| 5 | Operaciones de reserva / proceso de negocio | 5 | T18 – T22 |
| 6 | Errores y situaciones límite | 3 | T23 – T25 |

---

---

# Grupo 1 · Conversaciones Normales (T01 – T06)

---

## T01 — Consulta general de servicios/espacios

| Campo | Detalle |
|-------|---------|
| **Caso** | T01 · Consulta general de servicios/espacios |
| **Propósito** | Verificar que el chatbot responda correctamente a una consulta abierta sobre los servicios y espacios disponibles en el centro de convenciones. |
| **Grupo** | 1 — Conversaciones normales |
| **Cuenta utilizada** | Cuenta Telegram A (`@usuario_prueba_A`) |
| **Datos iniciales / Precondiciones** | Ninguna reserva previa necesaria. Bot activo y conectado. |
| **Entrada / Pasos** | 1. El usuario envía: `"¿Qué servicios ofrecen?"` |
| **Resultado esperado** | El bot responde con la lista de los 4 servicios disponibles: Conferencia Corporativa (EVT-CORP, Auditorio Nova, 4 h, máx. 100), Recepción de Boda (EVT-BODA, Salón Imperial, 5 h, máx. 200), Celebración de Cumpleaños (EVT-CUMP, Salón Social, 4 h, máx. 80) y Taller Ejecutivo (EVT-WORK, Sala Innovación, 2 h, máx. 30). Muestra información clara de cada espacio, duración y capacidad. |
| **Resultado obtenido** | El bot respondió con un mensaje formateado que presenta los 4 servicios con nombre, espacio asignado, duración y capacidad máxima. Incluye botones inline para seleccionar cada servicio. |
| **Cumplimiento** | ✅ **Sí** — Se despliegan correctamente los 4 servicios con toda la información requerida. |
| **Evidencia** | [`../evidencias/T01_servicios.png`](../evidencias/T01_servicios.png) |
| **Corrección (si aplica)** | Ninguna. |

---

## T02 — Consulta de precio de un servicio

| Campo | Detalle |
|-------|---------|
| **Caso** | T02 · Consulta de precio de un servicio |
| **Propósito** | Validar que el bot proporcione información de precios o tarifas cuando el usuario pregunta por el costo de un servicio específico. |
| **Grupo** | 1 — Conversaciones normales |
| **Cuenta utilizada** | Cuenta Telegram A (`@usuario_prueba_A`) |
| **Datos iniciales / Precondiciones** | Bot activo. No se requieren reservas previas. |
| **Entrada / Pasos** | 1. El usuario envía: `"¿Cuánto cuesta reservar una conferencia corporativa?"` |
| **Resultado esperado** | El bot responde con la información del servicio EVT-CORP (Conferencia Corporativa): espacio Auditorio Nova, duración 4 horas, capacidad máxima de 100 personas, y el precio o tarifa correspondiente. Si no maneja precios directos, indica que debe contactar al administrador o proporciona la información disponible. |
| **Resultado obtenido** | El bot identificó el servicio Conferencia Corporativa y respondió con los detalles del paquete: espacio (Auditorio Nova), duración (4 h), capacidad (100 personas) y la tarifa asociada. Ofreció proceder con la reserva. |
| **Cumplimiento** | ✅ **Sí** — El bot responde de forma precisa con la información de precio del servicio consultado. |
| **Evidencia** | [`../evidencias/T02_precio.png`](../evidencias/T02_precio.png) |
| **Corrección (si aplica)** | Ninguna. |

---

## T03 — Reserva completa en un solo mensaje

| Campo | Detalle |
|-------|---------|
| **Caso** | T03 · Reserva completa en un solo mensaje |
| **Propósito** | Verificar que el bot pueda procesar una reserva cuando el usuario proporciona todos los datos necesarios en un único mensaje (servicio, fecha, hora, número de asistentes, nombre y contacto). |
| **Grupo** | 1 — Conversaciones normales |
| **Cuenta utilizada** | Cuenta Telegram A (`@usuario_prueba_A`) |
| **Datos iniciales / Precondiciones** | Bot activo. No hay reservas existentes en el horario seleccionado para el espacio solicitado. |
| **Entrada / Pasos** | 1. El usuario envía: `"Quiero reservar una conferencia corporativa para el 10 de diciembre de 2026 a las 09:00, somos 50 personas, a nombre de Carlos Méndez, contacto: 0412-5551234"` |
| **Resultado esperado** | El bot extrae todos los campos del mensaje: servicio (EVT-CORP), fecha (2026-12-10), hora (09:00–13:00), asistentes (50), nombre (Carlos Méndez), contacto (0412-5551234). Presenta un resumen de la reserva y solicita confirmación. Al confirmar, genera el código NOVA-XXXX y lo registra en SQLite con estado "activa". |
| **Resultado obtenido** | El bot interpretó correctamente todos los datos del mensaje único. Mostró el resumen con los detalles y un botón de confirmación. Al presionar "✅ Confirmar", generó el código NOVA-0001 y confirmó la reserva. Se verificó el registro en la base de datos SQLite con estado "activa". |
| **Cumplimiento** | ✅ **Sí** — La reserva en un solo mensaje fue procesada completamente, con código generado y registro persistido en BD. |
| **Evidencia** | [`../evidencias/T03_reserva_completa.png`](../evidencias/T03_reserva_completa.png) |
| **Corrección (si aplica)** | Ninguna. |

---

## T04 — Reserva multi-turno (4 pasos)

| Campo | Detalle |
|-------|---------|
| **Caso** | T04 · Reserva multi-turno (4 pasos) |
| **Propósito** | Validar que el flujo conversacional guiado funcione correctamente: el bot solicita los datos faltantes paso a paso hasta completar la reserva (servicio → fecha → hora+asistentes → nombre/contacto → confirmación). |
| **Grupo** | 1 — Conversaciones normales |
| **Cuenta utilizada** | Cuenta Telegram A (`@usuario_prueba_A`) |
| **Datos iniciales / Precondiciones** | Bot activo. Sin reservas conflictivas en la fecha/hora que se elegirá. |
| **Entrada / Pasos** | 1. Usuario: `"Quiero hacer una reserva"` → Bot pregunta qué servicio desea. 2. Usuario selecciona: `"Recepción de Boda"` → Bot solicita fecha. 3. Usuario: `"15 de diciembre de 2026 a las 14:00, 150 personas"` → Bot solicita nombre y contacto. 4. Usuario: `"Ana López, teléfono 0414-7779999"` → Bot muestra resumen y solicita confirmación. 5. Usuario presiona: `"✅ Confirmar"`. |
| **Resultado esperado** | En cada paso el bot solicita únicamente la información faltante. El resumen final incluye: servicio EVT-BODA, Salón Imperial, fecha 2026-12-15, hora 14:00–19:00 (5 h), 150 asistentes, Ana López, 0414-7779999. Al confirmar, se genera NOVA-XXXX y se persiste en SQLite. |
| **Resultado obtenido** | El bot guió la conversación en 4 pasos correctamente. En cada turno solicitó solo los datos faltantes. El resumen final fue preciso. Al confirmar, generó el código NOVA-0002 con todos los datos correctos en la base de datos. Estado: "activa". |
| **Cumplimiento** | ✅ **Sí** — El flujo multi-turno completó los 4 pasos sin errores y persistió la reserva. |
| **Evidencia** | [`../evidencias/T04_multiturn.png`](../evidencias/T04_multiturn.png) |
| **Corrección (si aplica)** | Ninguna. |

---

## T05 — Saludo y navegación del menú

| Campo | Detalle |
|-------|---------|
| **Caso** | T05 · Saludo y navegación del menú |
| **Propósito** | Verificar que el bot responda apropiadamente a un saludo inicial y presente las opciones de navegación (menú principal) para que el usuario seleccione una acción. |
| **Grupo** | 1 — Conversaciones normales |
| **Cuenta utilizada** | Cuenta Telegram A (`@usuario_prueba_A`) |
| **Datos iniciales / Precondiciones** | Bot activo. Sesión limpia (sin conversación previa o tras /reiniciar). |
| **Entrada / Pasos** | 1. El usuario envía: `"Hola"` → Bot saluda y muestra menú. 2. El usuario selecciona la opción: `"📋 Ver servicios"`. |
| **Resultado esperado** | Al recibir el saludo, el bot responde con un mensaje de bienvenida al Centro de Convenciones NovaEventos y presenta un menú con opciones: ver servicios, hacer una reserva, consultar una reserva, cancelar una reserva. Al seleccionar "Ver servicios", muestra la lista de los 4 servicios disponibles. |
| **Resultado obtenido** | El bot respondió con: "¡Hola! 👋 Bienvenido/a a NovaEventos. ¿En qué puedo ayudarte?" y presentó botones de menú. Al seleccionar "📋 Ver servicios", desplegó la lista completa de los 4 servicios con sus detalles. |
| **Cumplimiento** | ✅ **Sí** — El saludo se manejó correctamente y la navegación del menú funcionó como se esperaba. |
| **Evidencia** | [`../evidencias/T05_saludo_menu.png`](../evidencias/T05_saludo_menu.png) |
| **Corrección (si aplica)** | Ninguna. |

---

## T06 — Consulta de disponibilidad de horario específico

| Campo | Detalle |
|-------|---------|
| **Caso** | T06 · Consulta de disponibilidad de un horario específico |
| **Propósito** | Verificar que el bot pueda informar si un espacio está disponible en una fecha y hora determinadas, consultando las reservas activas en la base de datos. |
| **Grupo** | 1 — Conversaciones normales |
| **Cuenta utilizada** | Cuenta Telegram A (`@usuario_prueba_A`) |
| **Datos iniciales / Precondiciones** | Existe la reserva NOVA-0001 (EVT-CORP, Auditorio Nova, 2026-12-10, 09:00–13:00, activa) creada en T03. |
| **Entrada / Pasos** | 1. El usuario envía: `"¿Está disponible el Auditorio Nova el 10 de diciembre de 2026 a las 10:00?"` |
| **Resultado esperado** | El bot consulta las reservas activas para el Auditorio Nova en la fecha 2026-12-10 y detecta el cruce con la reserva NOVA-0001 (09:00–13:00). Responde indicando que ese horario **no está disponible** y sugiere horarios alternativos (por ejemplo, a partir de las 13:00). |
| **Resultado obtenido** | El bot respondió: "El Auditorio Nova no está disponible el 10/12/2026 a las 10:00 ya que existe una reserva activa de 09:00 a 13:00. Te sugiero a partir de las 13:00. ¿Deseas reservar en otro horario?" |
| **Cumplimiento** | ✅ **Sí** — El bot detectó correctamente el cruce de horarios y sugirió alternativas. |
| **Evidencia** | [`../evidencias/T06_disponibilidad.png`](../evidencias/T06_disponibilidad.png) |
| **Corrección (si aplica)** | Ninguna. |

---

---

# Grupo 2 · Preguntas Ambiguas o Incompletas (T07 – T10)

---

## T07 — Mensaje sin servicio identificable

| Campo | Detalle |
|-------|---------|
| **Caso** | T07 · Mensaje sin servicio identificable |
| **Propósito** | Validar que el bot maneje adecuadamente un mensaje ambiguo donde no se puede determinar qué servicio desea el usuario, solicitando aclaración en lugar de asumir. |
| **Grupo** | 2 — Preguntas ambiguas o incompletas |
| **Cuenta utilizada** | Cuenta Telegram A (`@usuario_prueba_A`) |
| **Datos iniciales / Precondiciones** | Bot activo. Sesión limpia. |
| **Entrada / Pasos** | 1. El usuario envía: `"Quiero hacer algo el viernes"` |
| **Resultado esperado** | El bot reconoce la intención de reservar pero no puede identificar el servicio específico. Responde pidiendo al usuario que seleccione uno de los 4 servicios disponibles. Presenta los servicios como opciones (botones o lista). |
| **Resultado obtenido** | El bot respondió: "¡Con gusto te ayudo! Para avanzar con tu reserva, necesito saber qué tipo de evento deseas. Estos son nuestros servicios:" y presentó los 4 servicios con botones inline para seleccionar. |
| **Cumplimiento** | ✅ **Sí** — El bot no asumió un servicio y solicitó aclaración mostrando las opciones disponibles. |
| **Evidencia** | [`../evidencias/T07_sin_servicio.png`](../evidencias/T07_sin_servicio.png) |
| **Corrección (si aplica)** | Ninguna. |

---

## T08 — Fecha sin formato correcto

| Campo | Detalle |
|-------|---------|
| **Caso** | T08 · Fecha sin formato correcto |
| **Propósito** | Verificar que el bot interprete correctamente fechas en lenguaje natural (como "el próximo sábado" o "15 de diciembre") y las convierta al formato adecuado (YYYY-MM-DD). |
| **Grupo** | 2 — Preguntas ambiguas o incompletas |
| **Cuenta utilizada** | Cuenta Telegram A (`@usuario_prueba_A`) |
| **Datos iniciales / Precondiciones** | Bot activo. El usuario ya seleccionó un servicio (EVT-CUMP). |
| **Entrada / Pasos** | 1. (Contexto previo: el usuario ya indicó que quiere un Cumpleaños.) 2. Bot pregunta la fecha. 3. Usuario envía: `"para el próximo sábado"` |
| **Resultado esperado** | El bot calcula la fecha del próximo sábado a partir de la fecha actual y la presenta al usuario para confirmar (ej.: "Entendido, ¿te refieres al sábado 28 de noviembre de 2026?"). Si no puede interpretar la fecha con certeza, solicita al usuario que la especifique en formato DD/MM/AAAA. |
| **Resultado obtenido** | El bot interpretó "el próximo sábado" y respondió: "Entendido, el próximo sábado sería el 28/11/2026. ¿Es correcto?" con botones de "Sí" y "No, cambiar fecha". |
| **Cumplimiento** | ✅ **Sí** — El bot interpretó la fecha en lenguaje natural y pidió confirmación antes de proceder. |
| **Evidencia** | [`../evidencias/T08_fecha_natural.png`](../evidencias/T08_fecha_natural.png) |
| **Corrección (si aplica)** | Ninguna. |

---

## T09 — Número de asistentes no especificado

| Campo | Detalle |
|-------|---------|
| **Caso** | T09 · Número de asistentes no especificado |
| **Propósito** | Verificar que el bot solicite explícitamente el número de asistentes cuando el usuario proporciona servicio, fecha y hora pero omite la cantidad de personas. |
| **Grupo** | 2 — Preguntas ambiguas o incompletas |
| **Cuenta utilizada** | Cuenta Telegram A (`@usuario_prueba_A`) |
| **Datos iniciales / Precondiciones** | Bot activo. Sesión limpia. |
| **Entrada / Pasos** | 1. El usuario envía: `"Quiero reservar un taller ejecutivo para el 20 de diciembre de 2026 a las 10:00"` |
| **Resultado esperado** | El bot reconoce el servicio (EVT-WORK), la fecha (2026-12-20) y la hora (10:00), pero detecta que falta el número de asistentes. Solicita al usuario que indique cuántas personas asistirán (recordando que el máximo para Sala Innovación es 30). |
| **Resultado obtenido** | El bot respondió: "Perfecto, Taller Ejecutivo en Sala Innovación el 20/12/2026 a las 10:00. ¿Cuántas personas asistirán? (máximo 30 personas para este espacio)." |
| **Cumplimiento** | ✅ **Sí** — El bot detectó la ausencia del dato de asistentes y lo solicitó explícitamente, indicando el límite de capacidad. |
| **Evidencia** | [`../evidencias/T09_sin_asistentes.png`](../evidencias/T09_sin_asistentes.png) |
| **Corrección (si aplica)** | Ninguna. |

---

## T10 — Mensaje con múltiples intenciones

| Campo | Detalle |
|-------|---------|
| **Caso** | T10 · Mensaje con múltiples intenciones |
| **Propósito** | Verificar el comportamiento del bot cuando el usuario expresa dos intenciones distintas en un solo mensaje (dos reservas diferentes). |
| **Grupo** | 2 — Preguntas ambiguas o incompletas |
| **Cuenta utilizada** | Cuenta Telegram A (`@usuario_prueba_A`) |
| **Datos iniciales / Precondiciones** | Bot activo. Sesión limpia. |
| **Entrada / Pasos** | 1. El usuario envía: `"Quiero una boda y también un taller"` |
| **Resultado esperado** | El bot reconoce que hay dos intenciones distintas. Informa al usuario que el sistema procesa una reserva a la vez y le pide que elija cuál desea reservar primero: Recepción de Boda (EVT-BODA) o Taller Ejecutivo (EVT-WORK). |
| **Resultado obtenido** | El bot respondió: "Veo que te interesan dos servicios: Recepción de Boda y Taller Ejecutivo. Para brindarte la mejor atención, procesemos una reserva a la vez. ¿Cuál deseas reservar primero?" y mostró dos botones: "💒 Recepción de Boda" y "📊 Taller Ejecutivo". |
| **Cumplimiento** | ✅ **Sí** — El bot identificó las dos intenciones y guió al usuario a elegir una para procesar primero. |
| **Evidencia** | [`../evidencias/T10_multiples_intenciones.png`](../evidencias/T10_multiples_intenciones.png) |
| **Corrección (si aplica)** | Ninguna. |

---

---

# Grupo 3 · Contexto, Memoria y Estado (T11 – T14)

---

## T11 — Dos cuentas con solicitudes independientes

| Campo | Detalle |
|-------|---------|
| **Caso** | T11 · Dos cuentas con solicitudes independientes |
| **Propósito** | Verificar que el bot mantiene sesiones aisladas por cuenta de Telegram: dos usuarios diferentes pueden hacer reservas simultáneamente sin que los datos de uno afecten al otro. |
| **Grupo** | 3 — Contexto, memoria y estado |
| **Cuenta utilizada** | Cuenta Telegram A (`@usuario_prueba_A`) y Cuenta Telegram B (`@usuario_prueba_B`) |
| **Datos iniciales / Precondiciones** | Bot activo. Ambas cuentas con sesión limpia. Sin reservas previas conflictivas. |
| **Entrada / Pasos** | 1. **Cuenta A** envía: `"Quiero reservar una conferencia corporativa para el 12 de diciembre de 2026 a las 09:00, 80 personas, nombre: Pedro Ruiz, contacto: 0412-1112233"` → Confirma. 2. **Cuenta B** envía (simultáneamente): `"Quiero un cumpleaños para el 12 de diciembre de 2026 a las 15:00, 60 personas, nombre: Laura Díaz, contacto: 0414-4445566"` → Confirma. 3. Verificar que cada cuenta recibió su propio código NOVA-XXXX y que los registros en SQLite son independientes. |
| **Resultado esperado** | Cuenta A recibe NOVA-XXXX con EVT-CORP, Pedro Ruiz. Cuenta B recibe NOVA-XXXX diferente con EVT-CUMP, Laura Díaz. Los datos de un usuario no se filtran al otro. En la BD existen dos registros distintos con chat_id diferentes. |
| **Resultado obtenido** | Cuenta A obtuvo NOVA-0003 (EVT-CORP, Auditorio Nova, 12/12/2026, 09:00–13:00, Pedro Ruiz). Cuenta B obtuvo NOVA-0004 (EVT-CUMP, Salón Social, 12/12/2026, 15:00–19:00, Laura Díaz). Verificación en SQLite: dos registros con chat_id distintos, datos completamente aislados. |
| **Cumplimiento** | ✅ **Sí** — Las sesiones son completamente independientes; no hay filtración de datos entre cuentas. |
| **Evidencia** | [`../evidencias/T11_dos_cuentas.png`](../evidencias/T11_dos_cuentas.png) |
| **Corrección (si aplica)** | Ninguna. |

---

## T12 — Reinicio de sesión (/reiniciar)

| Campo | Detalle |
|-------|---------|
| **Caso** | T12 · Reinicio de sesión (/reiniciar) |
| **Propósito** | Verificar que el comando /reiniciar limpia el borrador de conversación actual pero NO elimina las reservas ya confirmadas en la base de datos. |
| **Grupo** | 3 — Contexto, memoria y estado |
| **Cuenta utilizada** | Cuenta Telegram A (`@usuario_prueba_A`) |
| **Datos iniciales / Precondiciones** | Cuenta A tiene reservas confirmadas previas (ej.: NOVA-0001, NOVA-0003). El usuario está a mitad de una nueva reserva (ya seleccionó servicio y fecha pero no ha confirmado). |
| **Entrada / Pasos** | 1. (Contexto: el usuario está a mitad del flujo de reserva, ya indicó servicio EVT-BODA y fecha 20/12/2026.) 2. El usuario envía: `/reiniciar` 3. Verificar que el borrador se limpió. 4. El usuario envía: `/consultar NOVA-0001` para verificar que la reserva previa sigue en la BD. |
| **Resultado esperado** | Al ejecutar /reiniciar: el bot confirma que la sesión se ha reiniciado y el borrador de la reserva en curso se elimina. Al consultar NOVA-0001: la reserva previa sigue existiendo en la BD con estado "activa" y todos sus datos intactos. |
| **Resultado obtenido** | El bot respondió: "🔄 Sesión reiniciada. Tu conversación ha sido limpiada. Las reservas confirmadas no se ven afectadas." Al ejecutar `/consultar NOVA-0001`, el bot mostró los detalles completos de la reserva (EVT-CORP, 10/12/2026, 09:00–13:00, Carlos Méndez) con estado "activa". |
| **Cumplimiento** | ✅ **Sí** — El reinicio limpió el borrador pero preservó las reservas confirmadas en la base de datos. |
| **Evidencia** | [`../evidencias/T12_reiniciar.png`](../evidencias/T12_reiniciar.png) |
| **Corrección (si aplica)** | Ninguna. |

---

## T13 — Cambio de dato en medio de la conversación

| Campo | Detalle |
|-------|---------|
| **Caso** | T13 · Cambio de dato en medio de la conversación |
| **Propósito** | Verificar que el bot permita al usuario cambiar un dato ya proporcionado (como la fecha o la hora) antes de confirmar la reserva, sin reiniciar todo el flujo. |
| **Grupo** | 3 — Contexto, memoria y estado |
| **Cuenta utilizada** | Cuenta Telegram A (`@usuario_prueba_A`) |
| **Datos iniciales / Precondiciones** | Bot activo. Sesión limpia. |
| **Entrada / Pasos** | 1. Usuario: `"Quiero reservar un cumpleaños"` → Bot pide fecha. 2. Usuario: `"5 de diciembre de 2026 a las 16:00, 40 personas"` → Bot pide nombre/contacto. 3. Usuario: `"Ah no, mejor que sea el 6 de diciembre a las 17:00"` → Bot debe actualizar la fecha y hora. 4. Usuario: `"María García, teléfono 0416-8889900"` → Bot muestra resumen. 5. Usuario confirma. |
| **Resultado esperado** | Al recibir la corrección en el paso 3, el bot actualiza la fecha a 2026-12-06 y la hora a 17:00–21:00 en el borrador, conservando los demás datos ya recopilados (servicio: EVT-CUMP, 40 asistentes). El resumen final refleja los datos corregidos. |
| **Resultado obtenido** | El bot detectó la corrección y respondió: "Entendido, actualizo la fecha al 06/12/2026 a las 17:00. Los demás datos se mantienen." El resumen final mostró: EVT-CUMP, Salón Social, 06/12/2026, 17:00–21:00, 40 personas, María García. Se generó NOVA-0005 con los datos correctos. |
| **Cumplimiento** | ✅ **Sí** — El bot permitió cambiar la fecha/hora sin perder los demás datos y el resumen final fue correcto. |
| **Evidencia** | [`../evidencias/T13_cambio_dato.png`](../evidencias/T13_cambio_dato.png) |
| **Corrección (si aplica)** | Ninguna. |

---

## T14 — Confirmación repetida / botón antiguo

| Campo | Detalle |
|-------|---------|
| **Caso** | T14 · Confirmación repetida / botón antiguo |
| **Propósito** | Verificar que el bot maneje correctamente una situación donde el usuario presiona el botón de confirmación más de una vez, o intenta usar un botón de una sesión anterior/expirada. |
| **Grupo** | 3 — Contexto, memoria y estado |
| **Cuenta utilizada** | Cuenta Telegram A (`@usuario_prueba_A`) |
| **Datos iniciales / Precondiciones** | Reserva NOVA-0005 ya fue confirmada exitosamente en T13. El botón "✅ Confirmar" de esa reserva sigue visible en el chat. |
| **Entrada / Pasos** | 1. El usuario presiona nuevamente el botón `"✅ Confirmar"` de la reserva ya completada (NOVA-0005). |
| **Resultado esperado** | El bot detecta que la reserva ya fue confirmada (o que la sesión de borrador ya no existe) y responde con un mensaje indicando que la acción ya fue procesada. No se crea una reserva duplicada en la BD. |
| **Resultado obtenido** | El bot respondió: "⚠️ Esta reserva ya fue confirmada anteriormente (NOVA-0005). No se realizó ninguna acción adicional." No se generó ningún registro duplicado en la base de datos. |
| **Cumplimiento** | ✅ **Sí** — El bot rechazó la confirmación duplicada y no creó registros repetidos en la BD. |
| **Evidencia** | [`../evidencias/T14_doble_confirmacion.png`](../evidencias/T14_doble_confirmacion.png) |
| **Corrección (si aplica)** | Ninguna. |

---

---

# Grupo 4 · Fuera del Dominio (T15 – T17)

---

## T15 — Pregunta no relacionada con el dominio

| Campo | Detalle |
|-------|---------|
| **Caso** | T15 · Pregunta no relacionada con el dominio |
| **Propósito** | Verificar que el bot responda apropiadamente a preguntas fuera del ámbito de reservas de eventos, redirigiendo al usuario a los servicios disponibles. |
| **Grupo** | 4 — Fuera del dominio |
| **Cuenta utilizada** | Cuenta Telegram A (`@usuario_prueba_A`) |
| **Datos iniciales / Precondiciones** | Bot activo. Sesión limpia. |
| **Entrada / Pasos** | 1. El usuario envía: `"¿Cuál es la capital de Francia?"` |
| **Resultado esperado** | El bot indica amablemente que solo puede asistir con temas relacionados al Centro de Convenciones NovaEventos y la reserva de eventos. Ofrece las opciones disponibles (ver servicios, hacer reserva, etc.). |
| **Resultado obtenido** | El bot respondió: "😊 Gracias por tu mensaje, pero solo puedo ayudarte con reservas y servicios del Centro de Convenciones NovaEventos. ¿Te gustaría ver nuestros servicios disponibles o hacer una reserva?" y mostró los botones del menú principal. |
| **Cumplimiento** | ✅ **Sí** — El bot rechazó cortésmente la pregunta fuera de dominio y redirigió al usuario a los servicios disponibles. |
| **Evidencia** | [`../evidencias/T15_fuera_dominio.png`](../evidencias/T15_fuera_dominio.png) |
| **Corrección (si aplica)** | Ninguna. |

---

## T16 — Intento de inyección (código/SQL)

| Campo | Detalle |
|-------|---------|
| **Caso** | T16 · Intento de inyección (código/SQL) |
| **Propósito** | Verificar que el bot sea resistente a intentos de inyección SQL o de código malicioso, y que no ejecute ni exponga datos sensibles. |
| **Grupo** | 4 — Fuera del dominio |
| **Cuenta utilizada** | Cuenta Telegram A (`@usuario_prueba_A`) |
| **Datos iniciales / Precondiciones** | Bot activo. Base de datos con reservas existentes. |
| **Entrada / Pasos** | 1. El usuario envía: `"Robert'); DROP TABLE reservas;--"` |
| **Resultado esperado** | El bot trata el mensaje como texto plano. No ejecuta la instrucción SQL. La tabla `reservas` sigue intacta en la base de datos. El bot responde normalmente (puede indicar que no entendió el mensaje o redirigir al menú). |
| **Resultado obtenido** | El bot respondió: "No logré entender tu solicitud. ¿Te gustaría ver nuestros servicios o hacer una reserva?" La tabla `reservas` fue verificada en SQLite y permanece intacta con todos los registros previos. No se ejecutó ninguna instrucción SQL maliciosa (el sistema usa consultas parametrizadas). |
| **Cumplimiento** | ✅ **Sí** — El intento de inyección SQL fue neutralizado; la BD permanece íntegra y el bot respondió normalmente. |
| **Evidencia** | [`../evidencias/T16_inyeccion_sql.png`](../evidencias/T16_inyeccion_sql.png) |
| **Corrección (si aplica)** | Ninguna. |

---

## T17 — Mensaje vacío o solo emojis

| Campo | Detalle |
|-------|---------|
| **Caso** | T17 · Mensaje vacío o solo emojis |
| **Propósito** | Verificar que el bot maneje correctamente mensajes que no contienen texto procesable: mensajes vacíos, solo espacios, o solo emojis. |
| **Grupo** | 4 — Fuera del dominio |
| **Cuenta utilizada** | Cuenta Telegram A (`@usuario_prueba_A`) |
| **Datos iniciales / Precondiciones** | Bot activo. Sesión limpia. |
| **Entrada / Pasos** | 1. El usuario envía: `"🎉🎂🥳"` (solo emojis, sin texto). |
| **Resultado esperado** | El bot no arroja error. Responde con un mensaje amigable indicando que no pudo interpretar la solicitud y ofrece las opciones del menú principal para que el usuario seleccione una acción. |
| **Resultado obtenido** | El bot respondió: "¡Veo que estás de ánimo festivo! 🎉 Sin embargo, no logré entender una solicitud específica. ¿En qué puedo ayudarte?" y mostró los botones del menú principal: Ver servicios, Hacer reserva, Consultar reserva. |
| **Cumplimiento** | ✅ **Sí** — El bot manejó el mensaje de solo emojis sin errores y ofreció opciones útiles al usuario. |
| **Evidencia** | [`../evidencias/T17_emojis.png`](../evidencias/T17_emojis.png) |
| **Corrección (si aplica)** | Ninguna. |

---

---

# Grupo 5 · Operaciones de Reserva / Proceso de Negocio (T18 – T22)

---

## T18 — Creación exitosa con registro en SQLite

| Campo | Detalle |
|-------|---------|
| **Caso** | T18 · Creación exitosa con registro en SQLite |
| **Propósito** | Verificar el flujo completo de creación de una reserva desde la conversación hasta su persistencia en la base de datos SQLite, validando todos los campos almacenados. |
| **Grupo** | 5 — Operaciones de reserva / proceso de negocio |
| **Cuenta utilizada** | Cuenta Telegram B (`@usuario_prueba_B`) |
| **Datos iniciales / Precondiciones** | Bot activo. Sin reservas conflictivas en el horario seleccionado. |
| **Entrada / Pasos** | 1. Usuario B: `"Quiero reservar un taller ejecutivo para el 18 de diciembre de 2026 a las 14:00, 25 personas, nombre: Roberto Sánchez, teléfono: 0424-3334455"` 2. Bot muestra resumen → Usuario presiona `"✅ Confirmar"`. 3. Verificar en SQLite: `SELECT * FROM reservas WHERE codigo = 'NOVA-XXXX';` |
| **Resultado esperado** | Se genera código NOVA-XXXX. En la BD: servicio=EVT-WORK, espacio=Sala Innovación, fecha=2026-12-18, hora_inicio=14:00, hora_fin=16:00 (2 h), asistentes=25, nombre=Roberto Sánchez, contacto=0424-3334455, estado=activa, chat_id=ID_cuenta_B. |
| **Resultado obtenido** | Se generó NOVA-0006. Consulta SQL verificada: todos los campos coinciden exactamente. Servicio: EVT-WORK, espacio: Sala Innovación, fecha: 2026-12-18, hora: 14:00–16:00, asistentes: 25, nombre: Roberto Sánchez, contacto: 0424-3334455, estado: activa. El chat_id corresponde a la Cuenta B. |
| **Cumplimiento** | ✅ **Sí** — La reserva se creó y persistió correctamente en SQLite con todos los campos verificados. |
| **Evidencia** | [`../evidencias/T18_registro_sqlite.png`](../evidencias/T18_registro_sqlite.png) |
| **Corrección (si aplica)** | Ninguna. |

---

## T19 — Consulta de reserva propia (/consultar NOVA-XXXX)

| Campo | Detalle |
|-------|---------|
| **Caso** | T19 · Consulta de reserva propia (/consultar NOVA-XXXX) |
| **Propósito** | Verificar que el comando /consultar permite a un usuario ver los detalles de su propia reserva activa usando el código NOVA-XXXX. |
| **Grupo** | 5 — Operaciones de reserva / proceso de negocio |
| **Cuenta utilizada** | Cuenta Telegram B (`@usuario_prueba_B`) |
| **Datos iniciales / Precondiciones** | Existe la reserva NOVA-0006 creada por la Cuenta B en T18 con estado "activa". |
| **Entrada / Pasos** | 1. Usuario B envía: `/consultar NOVA-0006` |
| **Resultado esperado** | El bot muestra los detalles completos de la reserva NOVA-0006: servicio (Taller Ejecutivo), espacio (Sala Innovación), fecha (18/12/2026), horario (14:00–16:00), asistentes (25), nombre (Roberto Sánchez), contacto (0424-3334455), estado (activa). |
| **Resultado obtenido** | El bot respondió con un mensaje formateado: "📋 **Reserva NOVA-0006** — Servicio: Taller Ejecutivo | Espacio: Sala Innovación | Fecha: 18/12/2026 | Horario: 14:00 – 16:00 | Asistentes: 25 | Nombre: Roberto Sánchez | Contacto: 0424-3334455 | Estado: ✅ Activa". |
| **Cumplimiento** | ✅ **Sí** — Todos los detalles de la reserva se mostraron correctamente al propietario. |
| **Evidencia** | [`../evidencias/T19_consultar.png`](../evidencias/T19_consultar.png) |
| **Corrección (si aplica)** | Ninguna. |

---

## T20 — Cancelación de reserva propia (/cancelar NOVA-XXXX)

| Campo | Detalle |
|-------|---------|
| **Caso** | T20 · Cancelación de reserva propia (/cancelar NOVA-XXXX) |
| **Propósito** | Verificar que el comando /cancelar permita al propietario cancelar su reserva activa, actualizando el estado en la BD y liberando el horario para futuras reservas. |
| **Grupo** | 5 — Operaciones de reserva / proceso de negocio |
| **Cuenta utilizada** | Cuenta Telegram B (`@usuario_prueba_B`) |
| **Datos iniciales / Precondiciones** | Existe la reserva NOVA-0006 (Cuenta B, EVT-WORK, 18/12/2026, 14:00–16:00, estado "activa"). |
| **Entrada / Pasos** | 1. Usuario B envía: `/cancelar NOVA-0006` 2. Bot solicita confirmación → Usuario presiona `"✅ Sí, cancelar"`. 3. Verificar en SQLite que el estado cambió a "cancelada". 4. Intentar reservar Sala Innovación el 18/12/2026 a las 14:00 para verificar que el horario quedó libre. |
| **Resultado esperado** | El bot confirma la cancelación de NOVA-0006. En la BD el estado cambia de "activa" a "cancelada". El horario 14:00–16:00 del 18/12/2026 en Sala Innovación queda disponible para nuevas reservas. |
| **Resultado obtenido** | El bot respondió: "⚠️ ¿Estás seguro de cancelar la reserva NOVA-0006?" → Al confirmar: "✅ La reserva NOVA-0006 ha sido cancelada exitosamente." Verificación en SQLite: estado = "cancelada". Se probó reservar el mismo horario y el sistema lo permitió (horario liberado). |
| **Cumplimiento** | ✅ **Sí** — La cancelación actualizó el estado en BD y liberó el horario correctamente. |
| **Evidencia** | [`../evidencias/T20_cancelar.png`](../evidencias/T20_cancelar.png) |
| **Corrección (si aplica)** | Ninguna. |

---

## T21 — Rechazo de cruce de horario

| Campo | Detalle |
|-------|---------|
| **Caso** | T21 · Rechazo de cruce de horario |
| **Propósito** | Verificar que el sistema rechace una reserva que se solaparía con una reserva activa existente en el mismo espacio, evitando conflictos de horario. |
| **Grupo** | 5 — Operaciones de reserva / proceso de negocio |
| **Cuenta utilizada** | Cuenta Telegram B (`@usuario_prueba_B`) |
| **Datos iniciales / Precondiciones** | Existe la reserva NOVA-0001 (Cuenta A, EVT-CORP, Auditorio Nova, 10/12/2026, 09:00–13:00, estado "activa"). |
| **Entrada / Pasos** | 1. Usuario B envía: `"Quiero reservar una conferencia corporativa para el 10 de diciembre de 2026 a las 11:00, 30 personas, nombre: Luis Torres, contacto: 0412-6667788"` |
| **Resultado esperado** | El bot detecta que el Auditorio Nova ya tiene una reserva activa (NOVA-0001) de 09:00 a 13:00 el 10/12/2026 y la nueva reserva (11:00–15:00) se solapa. Rechaza la solicitud e informa del conflicto. Sugiere horarios alternativos (ej.: a partir de las 13:00). |
| **Resultado obtenido** | El bot respondió: "❌ Lo siento, el Auditorio Nova no está disponible el 10/12/2026 de 11:00 a 15:00 debido a una reserva existente (09:00–13:00). Te sugiero reservar a partir de las 13:00. ¿Deseas elegir otro horario?" No se creó ningún registro nuevo en la BD. |
| **Cumplimiento** | ✅ **Sí** — El cruce de horario fue detectado y rechazado correctamente, sugiriendo alternativas. |
| **Evidencia** | [`../evidencias/T21_cruce_horario.png`](../evidencias/T21_cruce_horario.png) |
| **Corrección (si aplica)** | Ninguna. |

---

## T22 — Rechazo de acceso a reserva ajena

| Campo | Detalle |
|-------|---------|
| **Caso** | T22 · Rechazo de acceso a reserva ajena (/cancelar desde otra cuenta) |
| **Propósito** | Verificar que el sistema impida que un usuario cancele (o modifique) la reserva de otro usuario, validando la propiedad por chat_id de Telegram. |
| **Grupo** | 5 — Operaciones de reserva / proceso de negocio |
| **Cuenta utilizada** | Cuenta Telegram B (`@usuario_prueba_B`) intentando acceder a reserva de Cuenta A. |
| **Datos iniciales / Precondiciones** | Existe la reserva NOVA-0001 creada por la Cuenta A (EVT-CORP, 10/12/2026, estado "activa"). La Cuenta B NO es propietaria de NOVA-0001. |
| **Entrada / Pasos** | 1. Usuario B envía: `/cancelar NOVA-0001` |
| **Resultado esperado** | El bot verifica el chat_id del solicitante contra el chat_id del propietario de NOVA-0001. Como no coinciden, rechaza la operación con un mensaje indicando que solo el propietario puede cancelar su reserva. La reserva NOVA-0001 permanece activa e inalterada en la BD. |
| **Resultado obtenido** | El bot respondió: "🚫 No tienes permiso para cancelar esta reserva. Solo el propietario de la reserva NOVA-0001 puede realizar esta acción." Verificación en SQLite: NOVA-0001 sigue con estado "activa" y todos sus datos intactos. |
| **Cumplimiento** | ✅ **Sí** — El sistema rechazó el acceso a la reserva ajena y protegió la integridad de los datos. |
| **Evidencia** | [`../evidencias/T22_acceso_ajeno.png`](../evidencias/T22_acceso_ajeno.png) |
| **Corrección (si aplica)** | Ninguna. |

---

---

# Grupo 6 · Errores y Situaciones Límite (T23 – T25)

---

## T23 — Horario fuera del rango de atención

| Campo | Detalle |
|-------|---------|
| **Caso** | T23 · Horario fuera del rango de atención |
| **Propósito** | Verificar que el bot rechace una reserva cuya hora de finalización exceda el horario de operación (22:00). Por ejemplo, una Recepción de Boda (5 h) que inicie a las 19:00 terminaría a las 24:00, violando el límite. |
| **Grupo** | 6 — Errores y situaciones límite |
| **Cuenta utilizada** | Cuenta Telegram A (`@usuario_prueba_A`) |
| **Datos iniciales / Precondiciones** | Bot activo. No hay reservas previas en el horario solicitado. |
| **Entrada / Pasos** | 1. El usuario envía: `"Quiero reservar una recepción de boda para el 22 de diciembre de 2026 a las 19:00, 100 personas, nombre: Sofía Ramírez, contacto: 0416-1239876"` |
| **Resultado esperado** | El bot calcula que EVT-BODA dura 5 horas: 19:00 + 5 h = 24:00, lo cual excede el horario de cierre (22:00). Rechaza la solicitud y explica que el evento debe finalizar antes de las 22:00. Sugiere que la hora de inicio más tardía para una boda es las 17:00 (17:00 + 5 h = 22:00). |
| **Resultado obtenido** | El bot respondió: "❌ No es posible agendar una Recepción de Boda a las 19:00 ya que el evento finalizaría a las 24:00 y nuestro horario de operación es hasta las 22:00. Para un evento de 5 horas, la hora de inicio más tarde disponible es las 17:00. ¿Deseas reservar a las 17:00?" No se creó ningún registro en la BD. |
| **Cumplimiento** | ✅ **Sí** — El bot rechazó correctamente la reserva fuera de horario y sugirió la hora máxima de inicio válida. |
| **Evidencia** | [`../evidencias/T23_fuera_horario.png`](../evidencias/T23_fuera_horario.png) |
| **Corrección (si aplica)** | Ninguna. |

---

## T24 — Capacidad máxima excedida

| Campo | Detalle |
|-------|---------|
| **Caso** | T24 · Capacidad máxima excedida |
| **Propósito** | Verificar que el bot rechace una reserva cuando el número de asistentes supera la capacidad máxima del espacio seleccionado. |
| **Grupo** | 6 — Errores y situaciones límite |
| **Cuenta utilizada** | Cuenta Telegram A (`@usuario_prueba_A`) |
| **Datos iniciales / Precondiciones** | Bot activo. Sin reservas previas conflictivas. |
| **Entrada / Pasos** | 1. El usuario envía: `"Quiero un taller ejecutivo para el 19 de diciembre de 2026 a las 10:00, 150 personas, nombre: Andrés Flores, contacto: 0414-5556677"` |
| **Resultado esperado** | El bot detecta que el Taller Ejecutivo (EVT-WORK) se realiza en Sala Innovación con capacidad máxima de 30 personas. 150 asistentes exceden ampliamente este límite. Rechaza la solicitud, informa la capacidad máxima y sugiere un espacio alternativo con mayor capacidad (ej.: Auditorio Nova para 100, o Salón Imperial para 200). |
| **Resultado obtenido** | El bot respondió: "❌ La Sala Innovación (Taller Ejecutivo) tiene una capacidad máxima de 30 personas y has solicitado 150. No es posible procesar esta reserva. Para grupos de 150 personas, te sugiero: Salón Imperial (hasta 200 personas, Recepción de Boda). ¿Te gustaría reservar en otro espacio?" No se creó registro en la BD. |
| **Cumplimiento** | ✅ **Sí** — El bot rechazó la reserva por exceder la capacidad y sugirió alternativas apropiadas. |
| **Evidencia** | [`../evidencias/T24_capacidad_excedida.png`](../evidencias/T24_capacidad_excedida.png) |
| **Corrección (si aplica)** | Ninguna. |

---

## T25 — Reserva con código inexistente

| Campo | Detalle |
|-------|---------|
| **Caso** | T25 · Reserva con código inexistente |
| **Propósito** | Verificar que el bot responda apropiadamente cuando el usuario intenta consultar una reserva con un código NOVA-XXXX que no existe en la base de datos. |
| **Grupo** | 6 — Errores y situaciones límite |
| **Cuenta utilizada** | Cuenta Telegram A (`@usuario_prueba_A`) |
| **Datos iniciales / Precondiciones** | Bot activo. No existe ninguna reserva con código NOVA-9999 en la base de datos. |
| **Entrada / Pasos** | 1. El usuario envía: `/consultar NOVA-9999` |
| **Resultado esperado** | El bot busca NOVA-9999 en la tabla de reservas de SQLite y no encuentra resultados. Responde indicando que no existe una reserva con ese código y sugiere verificar el código o consultar las reservas activas del usuario. |
| **Resultado obtenido** | El bot respondió: "🔍 No se encontró ninguna reserva con el código NOVA-9999. Por favor verifica que el código sea correcto. Si necesitas ayuda, puedo mostrar tus reservas activas." No se produjo ningún error técnico ni excepción. |
| **Cumplimiento** | ✅ **Sí** — El bot manejó el código inexistente sin errores y ofreció alternativas útiles al usuario. |
| **Evidencia** | [`../evidencias/T25_codigo_inexistente.png`](../evidencias/T25_codigo_inexistente.png) |
| **Corrección (si aplica)** | Ninguna. |

---

---

## 📈 Resumen Ejecutivo de Resultados

| Métrica | Valor |
|---------|-------|
| **Total de pruebas** | 25 |
| **Pruebas aprobadas** | 25 ✅ |
| **Pruebas fallidas** | 0 ❌ |
| **Tasa de aprobación** | **100 %** |
| **Grupos evaluados** | 6 / 6 |

### Desglose por Grupo

| Grupo | Nombre | Aprobadas | Total | Estado |
|-------|--------|:---------:|:-----:|:------:|
| 1 | Conversaciones normales | 6 | 6 | ✅ |
| 2 | Preguntas ambiguas o incompletas | 4 | 4 | ✅ |
| 3 | Contexto, memoria y estado | 4 | 4 | ✅ |
| 4 | Fuera del dominio | 3 | 3 | ✅ |
| 5 | Operaciones de reserva / proceso de negocio | 5 | 5 | ✅ |
| 6 | Errores y situaciones límite | 3 | 3 | ✅ |

---

## 📌 Conclusiones

1. **Cobertura completa:** Las 25 pruebas cubren los 6 grupos requeridos, abarcando desde flujos conversacionales normales hasta situaciones límite y de seguridad.

2. **Robustez del chatbot:** El sistema maneja adecuadamente mensajes ambiguos, fechas en lenguaje natural, múltiples intenciones y entradas no válidas sin generar errores técnicos.

3. **Integridad de datos:** Las operaciones CRUD (crear, leer, cancelar) funcionan correctamente sobre la base de datos SQLite, con validaciones de cruce de horario, capacidad máxima y propiedad de reserva.

4. **Seguridad:** Los intentos de inyección SQL son neutralizados gracias al uso de consultas parametrizadas. El aislamiento de sesiones por chat_id garantiza la privacidad entre usuarios.

5. **Experiencia de usuario:** El bot mantiene un tono amigable y profesional, ofrece alternativas cuando rechaza solicitudes, y guía al usuario en cada paso del proceso.

---

> **Documento generado como parte de la entrega final del Proyecto NovaEventos.**  
> Véase también: [Bitácora Consolidada](./Bitacora_Consolidada.md) · [README.md](../README.md)
