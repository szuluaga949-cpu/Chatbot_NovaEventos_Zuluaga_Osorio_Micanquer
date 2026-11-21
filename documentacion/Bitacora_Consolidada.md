# 📘 Bitácora Consolidada · Proyecto NovaEventos (Entrega Final)

**Asignatura:** Creación de Chatbots con IA · EAM 2026-II  
**Proyecto:** NovaEventos — Sistema Conversacional de Reservas para Centro de Eventos  
**Integrantes:** Santiago Zuluaga · Jefrey Osorio · Juan Micanquer  
**Versión documentada:** 3.0.0 (Entrega Final — Tercer Corte)  
**Fecha del documento:** 2026-11-21

**Enlaces rápidos del repositorio:**

- 📄 [README.md](../README.md)
- 📊 [Matriz de 25 Pruebas](./Matriz_25_Pruebas.md)
- 🎞️ [Presentación Final](../presentacion/Presentacion_Final.pdf)
- 🖼️ [Carpeta de Evidencias](../evidencias/)

---

## Tabla de Contenido

1. [Contexto, Problema y Alcance del Sistema](#1-contexto-problema-y-alcance-del-sistema)
2. [Arquitectura y Archivos](#2-arquitectura-y-archivos)
3. [Contexto, Memoria y Estado](#3-contexto-memoria-y-estado)
4. [Consumo del Modelo de Lenguaje (LLM)](#4-consumo-del-modelo-de-lenguaje-llm)
5. [Operaciones y Validaciones](#5-operaciones-y-validaciones)
6. [Evolución y Decisiones de Diseño](#6-evolución-y-decisiones-de-diseño)
7. [Pruebas y Evidencias](#7-pruebas-y-evidencias)
8. [Fallos y Correcciones](#8-fallos-y-correcciones)
9. [Limitaciones y Pendientes](#9-limitaciones-y-pendientes)
10. [Comparación Técnica: Flowise vs. Gradio vs. Telegram](#10-comparación-técnica-versión-primer-corte-flowise-vs-segundo-corte-gradio-vs-tercer-corte-telegram)

---

## 1. Contexto, Problema y Alcance del Sistema

### 1.1 Descripción del negocio

**NovaEventos** es un centro de convenciones y eventos sociales, corporativos y académicos que administra **cuatro espacios físicos** con reglas estrictas de horario de operación (**08:00 a 22:00**), duración fija por bloque de servicio y aforo máximo por salón. El catálogo de servicios se almacena en `catalogo_eventos.json`:

| ID | Servicio | Espacio | Duración | Capacidad Máxima |
|:---|:---|:---|:---:|:---:|
| `EVT-CORP` | Conferencia Corporativa | Auditorio Nova | 4 h | 100 personas |
| `EVT-BODA` | Recepción de Boda / Gala Social | Salón Imperial | 5 h | 200 personas |
| `EVT-CUMP` | Celebración de Cumpleaños | Salón Social | 4 h | 80 personas |
| `EVT-WORK` | Taller Ejecutivo / Workshop | Sala Innovación | 2 h | 30 personas |

Cada servicio tiene una **duración fija** que determina automáticamente la `hora_fin` del evento a partir de la `hora_inicio` seleccionada por el usuario:

$$\text{hora\_fin} = \text{hora\_inicio} + \text{duracion\_horas}$$

### 1.2 Problema que resuelve

Durante la gestión tradicional de reservas y en el prototipo inicial del primer corte (basado en Flowise + archivos JSON planos), se presentaban cuatro problemas críticos:

1. **Cruces de horarios (sobreasignación):** Al no calcular automáticamente la hora de finalización según la duración del servicio, se agendaban eventos que se traslapaban parcialmente en el mismo salón.
2. **Pérdida de contexto entre turnos:** Si el cliente entregaba los datos en tres o cuatro mensajes separados, el bot olvidaba la fecha o el salón mencionados al inicio.
3. **Ausencia de confirmación previa:** Las operaciones se ejecutaban sin pedir validación explícita al usuario, impidiendo corregir o descartar un borrador antes de escribir en la base de datos.
4. **Falta de persistencia transaccional:** Al cancelar una reserva se requería liberar el horario para nuevos clientes sin borrar el registro histórico.

### 1.3 Usuarios del sistema

| Usuario | Canal | Funciones principales |
|:---|:---|:---|
| **Clientes externos** (organizadores de eventos, empresas, particulares) | Bot de **Telegram** (tercer corte) o interfaz web **Gradio** (segundo corte) | Consultar catálogo, verificar disponibilidad, crear reservas, cancelarlas |
| **Coordinadores de NovaEventos** | API REST (Swagger UI) + Consola SQLite | Revisar tabla de reservas en tiempo real, auditar registros activos y cancelados |

### 1.4 Funciones implementadas

- Conversación natural en **múltiples turnos** recolectando progresivamente los 6 datos obligatorios de una reserva.
- Manejo de **sesiones independientes** en paralelo, aisladas por `chat_id` (Telegram) o `session_id` (Gradio).
- Validación matemática de **horario de apertura/cierre** (08:00–22:00), **aforo máximo** por salón y **rechazo de intervalos traslapados**.
- **CRUD completo** de reservas: Crear (`POST`), Consultar (`GET`), Modificar (`PUT`) y Cancelar lógica (`DELETE`).
- **Verificación de propiedad** en Telegram: solo el creador de una reserva puede cancelarla.
- **Teclados inline** en Telegram para confirmar o cancelar reservas con botones interactivos.
- **Fallback determinista** cuando el LLM no responde: extractor basado en expresiones regulares.

### 1.5 Limitaciones actuales

- **Duración fija por paquete:** Cada servicio tiene una duración predefinida (2, 4 o 5 h); no se ofrecen fracciones horarias.
- **Sin pasarela de pagos:** El sistema no procesa cobros en línea.
- **Sesiones/borradores en RAM:** Las reservas confirmadas persisten en SQLite, pero los borradores no confirmados se pierden al reiniciar el proceso.
- **Sin confirmación por email:** No se envía correo electrónico de confirmación al usuario.

---

## 2. Arquitectura y Archivos

### 2.1 Diagrama de arquitectura (Tercer Corte — Telegram)

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│                        USUARIO DE TELEGRAM                                   │
│                      (Envía mensajes / Comandos)                             │
└──────────────────────────────┬───────────────────────────────────────────────┘
                               │  Telegram Bot API (polling)
                               ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                      bot_telegram.py (Polling)                               │
│  - Recibe Update de Telegram                                                 │
│  - Enruta comandos: /start, /ayuda, /reservas, /consultar, /cancelar         │
│  - Muestra InlineKeyboards para confirmación (✅ Sí / ❌ Cancelar)           │
│  - Convierte respuestas a MarkdownV2 con _escapar_md()                       │
└──────────────────────────────┬───────────────────────────────────────────────┘
                               │  Llamada directa en Python
                               ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                     api_telegram.py (Adaptador)                              │
│  - Convierte chat_id → session_id ("tg_{chat_id}")                           │
│  - Detecta código NOVA-XXXX en respuestas → registra propiedad              │
│  - Detecta palabra "confirmas" → flag mostrar_confirmacion                   │
│  - Formatea respuestas Markdown → MarkdownV2 Telegram                        │
└────────────┬──────────────────────────────────┬──────────────────────────────┘
             │  Motor conversacional             │  Consultas directas DB
             ▼                                   ▼
┌──────────────────────────────┐  ┌────────────────────────────────────────────┐
│   consulta_llm.py (Motor)    │  │        chatbot_memoria.py (Sesiones)       │
│  - _sesiones: Dict en RAM    │  │  - _sesiones: Dict estado sesión           │
│  - Extractor determinista    │  │  - _reservas_por_usuario: Dict propiedad   │
│    (regex para slots)        │  │  - registrar_reserva_usuario()             │
│  - Lógica de flujo:          │  │  - es_propietario(sid, codigo)             │
│    servicio → fecha → hora   │  │  - obtener_reservas_usuario(sid)           │
│    → asistentes → cliente    │  └────────────────────────────────────────────┘
│  - Confirmación / descarte   │
│  - Consumo de API Groq       │
│  - _llamar_api() → FastAPI   │
└──────────────────────────────┘
             │  Peticiones HTTP REST
             │  GET / POST / DELETE
             ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│               main.py — API REST en FastAPI (puerto 8011)                    │
│  - GET  /health                    GET  /catalogo                            │
│  - GET  /disponibilidad            GET  /reservas  /reservas/{codigo}         │
│  - POST /reservas (201 / 409)      PUT  /reservas/{codigo}                   │
│  - DELETE /reservas/{codigo}                                                 │
│  - Validación de esquemas con Pydantic (ReservaCrearInput, Modificar...)     │
│  - Lifespan → inicializar_bd()                                               │
└──────────────────────────────┬───────────────────────────────────────────────┘
                               │  Llamada a funciones de persistencia
                               ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│              almacen_sqlite.py (Persistencia + Reglas de negocio)             │
│  - cargar_catalogo() → catalogo_eventos.json                                 │
│  - verificar_disponibilidad(excluir_codigo=...)                              │
│  - crear_reserva_db()   → BEGIN IMMEDIATE + INSERT + COMMIT                  │
│  - modificar_reserva_db() → BEGIN IMMEDIATE + UPDATE + COMMIT                │
│  - cancelar_reserva_db() → estado = 'cancelada'                              │
│  - Fórmula de cruce: inicio_nuevo < fin_exist AND fin_nuevo > inicio_exist   │
│  - Valida horario 08:00–22:00, aforo máximo, formato de fecha                │
└──────────────────────────────┬───────────────────────────────────────────────┘
                               │
                               ▼
                      ┌─────────────────┐
                      │   reservas.db   │
                      │    (SQLite)     │
                      └─────────────────┘
```

### 2.2 Interfaz alternativa: Gradio (segundo corte)

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│                 app_gradio.py — Interfaz Web (puerto 7860)                    │
│  - Tab "Asistente IA de Reservas": Chatbot + selector de sesión              │
│  - Tab "Panel de Reservas": Tabla gr.Dataframe + cancelación UI              │
│  - Llama directamente a consulta_llm.procesar_mensaje()                      │
│  - Consulta almacen_sqlite.listar_reservas_db() para la tabla                │
└──────────────────────────────────────────────────────────────────────────────┘
```

### 2.3 Responsabilidad de cada archivo

| Archivo | Líneas | Responsabilidad |
|:---|:---:|:---|
| `main.py` | 132 | API REST en FastAPI (puerto 8011). Define endpoints CRUD, valida esquemas con Pydantic (`ReservaCrearInput`, `ReservaModificarInput`), inicializa la BD al arrancar con `lifespan`. |
| `bot_telegram.py` | 198 | Bot de Telegram en modo polling. Registra handlers de comandos (`/start`, `/ayuda`, `/reservas`, `/consultar`, `/cancelar`, `/todas`, `/reiniciar`), muestra teclados inline para confirmación (`InlineKeyboardMarkup`), convierte respuestas a MarkdownV2. |
| `api_telegram.py` | 252 | Adaptador entre Telegram y el motor conversacional. Convierte `chat_id` → `session_id` (`tg_{chat_id}`), detecta creación de reservas para registrar propiedad, verifica ownership en cancelaciones, escapa caracteres especiales para MarkdownV2. |
| `consulta_llm.py` | 301 | Motor de conversación y extractor de entidades. Gestiona sesiones en RAM, extrae slots con regex (servicio, fecha, hora, asistentes, cliente), valida disponibilidad en tiempo real, gestiona flujo de confirmación, se comunica con la API REST vía `httpx`. |
| `chatbot_memoria.py` | 83 | Gestión de memoria y propiedad de reservas. Almacena estado de sesiones, mapea `session_id` → códigos de reserva creados (`_reservas_por_usuario`), verifica propiedad con `es_propietario()`. |
| `almacen_sqlite.py` | 465 | Capa de persistencia y reglas de negocio. Crea la tabla `reservas`, genera códigos `NOVA-XXXX` secuenciales, calcula intervalos horarios, valida cruces con la fórmula de solapamiento, ejecuta transacciones `BEGIN IMMEDIATE`. |
| `catalogo_eventos.json` | 34 | Catálogo de servicios del negocio: 4 servicios con sus IDs, nombres, espacios, duraciones y capacidades máximas. Horario de operación: 08:00–22:00. |
| `app_gradio.py` | 182 | Interfaz web en Gradio (segundo corte). Dos pestañas: chat interactivo + panel de reservas con tabla en vivo. Permite crear, consultar y cancelar reservas desde el navegador. |
| `simular_respuesta_perdida.py` | 84 | Script de prueba de fallback offline. Desactiva la clave de Groq y ejecuta una conversación completa para verificar que el extractor determinista funciona sin LLM. |
| `test_sistema_eventos.py` | 96 | Suite de pruebas automatizadas con `pytest`. Verifica conversación multi-turno, aislamiento de sesiones, rechazo de cruces y cancelación mediante `TestClient` de FastAPI. |

### 2.4 Esquema de la base de datos SQLite (`reservas.db`)

```sql
CREATE TABLE IF NOT EXISTS reservas (
    codigo TEXT PRIMARY KEY,                              -- NOVA-1001, NOVA-1002, ...
    cliente_nombre TEXT NOT NULL,                         -- "Camila Restrepo"
    cliente_contacto TEXT NOT NULL,                       -- "3001234567"
    servicio_id TEXT NOT NULL,                            -- "EVT-CORP"
    servicio_nombre TEXT NOT NULL,                        -- "Conferencia Corporativa"
    espacio TEXT NOT NULL,                                -- "Auditorio Nova"
    fecha TEXT NOT NULL,                                  -- "2026-11-15"
    hora_inicio TEXT NOT NULL,                            -- "09:00"
    duracion_horas INTEGER NOT NULL,                     -- 4
    hora_fin TEXT NOT NULL,                               -- "13:00"
    asistentes INTEGER NOT NULL,                         -- 90
    estado TEXT NOT NULL CHECK(estado IN ('activa', 'cancelada')),
    notas TEXT DEFAULT '',                                -- Observaciones
    creado_en TEXT NOT NULL,                              -- ISO 8601
    actualizado_en TEXT NOT NULL                          -- ISO 8601
);
```

La base de datos se inicializa automáticamente al arrancar FastAPI. Si la tabla está vacía, se insertan **3 reservas semilla**:

| Código | Cliente | Servicio | Espacio | Fecha | Horario | Estado |
|:---|:---|:---|:---|:---|:---|:---|
| `NOVA-1001` | Camila Restrepo | Conferencia Corporativa | Auditorio Nova | 2026-11-15 | 09:00–13:00 | activa |
| `NOVA-1002` | Andrés Mejía | Recepción de Boda | Salón Imperial | 2026-11-20 | 16:00–21:00 | activa |
| `NOVA-1003` | Laura Gómez | Taller Ejecutivo | Sala Innovación | 2026-11-15 | 14:00–16:00 | cancelada |

---

## 3. Contexto, Memoria y Estado

### 3.1 Separación de sesiones por `chat_id` / `session_id`

El sistema utiliza un esquema de sesiones completamente aisladas. Cada usuario tiene su propio espacio de trabajo independiente:

- **En Telegram:** El `chat_id` numérico se transforma en un `session_id` textual mediante la función `_session_id_telegram()`:

```python
def _session_id_telegram(chat_id: int) -> str:
    return f"tg_{chat_id}"
```

- **En Gradio:** El usuario selecciona manualmente un `session_id` (por ejemplo: `"usuario_principal"`) en un campo de texto.

Cada sesión almacena en `consulta_llm._sesiones` un diccionario con los **slots del borrador** (servicio, fecha, hora, asistentes, nombre, contacto, notas):

```python
_sesiones["tg_123456789"] = {
    "servicio_id": "EVT-CORP",
    "fecha": "2026-12-01",
    "hora_inicio": "10:00",
    "asistentes": 60,
    "cliente_nombre": None,     # ← aún falta
    "cliente_contacto": None,   # ← aún falta
    "notas": "",
    "borrador": ...  # referencia a sí mismo (compatibilidad)
}
```

Paralelamente, `chatbot_memoria.py` mantiene un segundo diccionario `_reservas_por_usuario` que mapea cada `session_id` al conjunto de códigos de reserva creados desde esa cuenta:

```python
_reservas_por_usuario = {
    "tg_123456789": {"NOVA-1004", "NOVA-1005"},
    "tg_987654321": {"NOVA-1006"},
}
```

### 3.2 ¿Qué sucede al reiniciar el proceso?

| Componente | Almacenamiento | Efecto al reiniciar |
|:---|:---|:---|
| **Reservas confirmadas** | SQLite en disco (`reservas.db`) | ✅ Persisten intactas |
| **Borradores no confirmados** | Diccionario en RAM (`_sesiones`) | ❌ Se pierden |
| **Propiedad de reservas** | Diccionario en RAM (`_reservas_por_usuario`) | ❌ Se pierde — el usuario no podrá cancelar las reservas que creó antes del reinicio |
| **Historial de chat** | Diccionario en RAM | ❌ Se pierde |

### 3.3 Acumulación incremental del borrador entre turnos

El motor conversacional en `consulta_llm.py` **nunca sobrescribe un slot ya capturado con `None`**. La lógica de extracción opera de forma **aditiva**: cada turno del usuario solo puede agregar o modificar campos, nunca borrarlos accidentalmente.

**Ejemplo de acumulación a lo largo de 4 turnos:**

```text
Turno 1: "Quiero una conferencia para el 2026-12-01"
  → servicio_id = "EVT-CORP", fecha = "2026-12-01"

Turno 2: "A las 10:00 para 60 personas"
  → hora_inicio = "10:00", asistentes = 60  (servicio y fecha se conservan)

Turno 3: "Santiago Zuluaga, 3005551122"
  → cliente_nombre = "Santiago Zuluaga", cliente_contacto = "3005551122"

Turno 4: "Sí, confirmo"
  → Se ejecuta POST /reservas → NOVA-1004 creada
```

La protección contra el borrado accidental se implementa con condicionales explícitos. Por ejemplo, para la fecha:

```python
if m_fecha and (not sesion["fecha"] or "fecha" in texto_lower):
    sesion["fecha"] = m_fecha.group(1)
```

Solo se actualiza si (a) no había fecha previa, o (b) el usuario menciona explícitamente la palabra "fecha" (indicando que desea cambiarla).

---

## 4. Consumo del Modelo de Lenguaje (LLM)

### 4.1 Endpoint, headers y credenciales

El módulo `consulta_llm.py` puede comunicarse con la API de **Groq** cuando la variable `GROQ_API_KEY` está configurada. Las variables de entorno relevantes son:

| Variable | Valor | Descripción |
|:---|:---|:---|
| `GROQ_API_KEY` | `gsk_********************************` | Token privado de Groq |
| `GROQ_MODEL` | `llama-3.3-70b-versatile` | Modelo LLM utilizado |
| `CHATBOT_API_URL` | `http://127.0.0.1:8011` | URL de la API FastAPI |
| `SQLITE_DB_PATH` | `reservas.db` | Ruta del archivo SQLite |
| `TELEGRAM_BOT_TOKEN` | Token de @BotFather | Token del bot de Telegram |

**Endpoint HTTP del LLM:**

```
POST https://api.groq.com/openai/v1/chat/completions
```

**Headers enviados:**

```json
{
  "Authorization": "Bearer gsk_********************************",
  "Content-Type": "application/json"
}
```

### 4.2 Estructura del payload

El payload enviado al modelo incluye:
- Dos mensajes `system`: el catálogo del negocio y el estado actual del borrador.
- Los últimos mensajes del historial (`user`/`assistant`).
- El mensaje nuevo del usuario.
- Se fuerza respuesta JSON con `"response_format": {"type": "json_object"}` y baja temperatura (`0.1`).

```json
{
  "model": "llama-3.3-70b-versatile",
  "temperature": 0.1,
  "response_format": { "type": "json_object" },
  "messages": [
    {
      "role": "system",
      "content": "Eres el asistente de reservas de NovaEventos. Horario: 08:00–22:00. Catálogo: EVT-CORP | Conferencia Corporativa | Auditorio Nova | 4h | 100 pers. ..."
    },
    {
      "role": "system",
      "content": "Estado del borrador de la sesión: {\"servicio_id\": \"EVT-CORP\", \"fecha\": \"2026-12-01\", \"hora_inicio\": null, ...}"
    },
    { "role": "user", "content": "Quiero una conferencia para el 2026-12-01" },
    { "role": "assistant", "content": "¿A qué hora deseas iniciar? (08:00–22:00)" },
    { "role": "user", "content": "A las 10:00 para 60 personas" }
  ]
}
```

### 4.3 Formato de respuesta JSON del modelo

```json
{
  "accion": "crear",
  "servicio_id": "EVT-CORP",
  "fecha": "2026-12-01",
  "hora_inicio": "10:00",
  "asistentes": 60,
  "cliente_nombre": null,
  "cliente_contacto": null,
  "notas": null,
  "confirmacion": "ninguna",
  "respuesta_asistente": "He registrado 10:00 y 60 asistentes. Indícame tu nombre y contacto."
}
```

### 4.4 Fallback determinista cuando el LLM falla

Cuando la API de Groq no está disponible (clave vacía, error de red, timeout), el motor **no se detiene**. El módulo `consulta_llm.py` contiene un **extractor determinista basado en expresiones regulares** que procesa cada mensaje del usuario sin depender del LLM:

```python
# Extracción de servicio
if any(k in texto_lower for k in ["conferencia", "corp", "auditorio"]):
    sesion["servicio_id"] = "EVT-CORP"

# Extracción de fecha (YYYY-MM-DD)
m_fecha = re.search(r"\b(\d{4}-\d{2}-\d{2})\b", texto)
if m_fecha:
    sesion["fecha"] = m_fecha.group(1)

# Extracción de hora (HH:MM)
m_hora = re.search(r"\b([01]?\d|2[0-3]):([0-5]\d)\b", texto)

# Extracción de asistentes
m_asist = re.search(r"\b(\d{1,4})\s*(?:asistentes|personas|invitados)\b", texto)
```

El script `simular_respuesta_perdida.py` verifica este comportamiento ejecutando una conversación completa de 4 turnos con `GROQ_API_KEY = ""` y verificando que todas las respuestas sean coherentes.

---

## 5. Operaciones y Validaciones

### 5.1 Flujo de confirmación de reservas

El proceso de creación de una reserva sigue un **flujo paso a paso** con confirmación explícita:

```text
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌────────────┐    ┌──────────┐    ┌────────────┐
│ Servicio │───▶│  Fecha   │───▶│   Hora   │───▶│ Asistentes │───▶│ Cliente  │───▶│ Confirmar  │
│ (slot 1) │    │ (slot 2) │    │ (slot 3) │    │  (slot 4)  │    │ (slot 5) │    │ (decisión) │
└──────────┘    └──────────┘    └──────────┘    └────────────┘    └──────────┘    └──────┬─────┘
                                                                                        │
                                                              ┌─────────────────────────┤
                                                              │                         │
                                                        ✅ "Sí"                    ❌ "Cancelar"
                                                              │                         │
                                                              ▼                         ▼
                                                     POST /reservas            reiniciar_sesion()
                                                     → NOVA-XXXX              → Borrador limpio
```

**Validación inmediata de disponibilidad:** Tan pronto como se tienen los 3 primeros slots (servicio + fecha + hora), el motor consulta `verificar_disponibilidad()` **antes** de pedir los datos del cliente. Si hay conflicto, se rechaza de inmediato:

```python
if sesion["servicio_id"] and sesion["fecha"] and sesion["hora_inicio"]:
    disp = consultar_disponibilidad_servicio(...)
    if not disp.get("disponible", True):
        sesion["hora_inicio"] = None  # Reset solo la hora
        return f"⚠️ Horario no disponible: {motivo}"
```

### 5.2 Endpoints de la API REST (`main.py`)

| Método | Ruta | Parámetros | Códigos HTTP | Operación |
|:---|:---|:---|:---:|:---|
| `GET` | `/health` | — | `200` | Verifica estado de la API y motor SQLite |
| `GET` | `/catalogo` | — | `200` | Retorna `catalogo_eventos.json` completo |
| `GET` | `/disponibilidad` | Query: `servicio_id`, `fecha`, `hora_inicio` | `200` | Verifica si el espacio está libre |
| `GET` | `/reservas` | Query opcional: `fecha`, `estado` | `200` | Lista reservas con filtros |
| `GET` | `/reservas/{codigo}` | Path: `codigo` | `200` / `404` | Consulta una reserva por código |
| `POST` | `/reservas` | Body JSON (`ReservaCrearInput`) | `201` / `409` | Crea reserva en transacción |
| `PUT` | `/reservas/{codigo}` | Path + Body (`ReservaModificarInput`) | `200` / `404` / `409` | Modifica reserva excluyendo auto-conflicto |
| `DELETE` | `/reservas/{codigo}` | Path: `codigo` | `200` / `404` | Cancelación lógica (`estado → 'cancelada'`) |

### 5.3 Comandos de Telegram (`bot_telegram.py`)

| Comando | Función | Descripción |
|:---|:---|:---|
| `/start` | `handler_start` | Bienvenida + reinicio de sesión |
| `/ayuda` (`/help`) | `handler_ayuda` | Muestra ayuda completa con lista de comandos |
| `/reiniciar` | `handler_reiniciar` | Limpia el borrador y el historial de la sesión |
| `/reservas` | `handler_reservas` | Muestra las reservas creadas por este usuario |
| `/todas` | `handler_todas` | Lista todas las reservas activas del sistema |
| `/consultar NOVA-XXXX` | `handler_consultar` | Muestra detalles completos de una reserva |
| `/cancelar NOVA-XXXX` | `handler_cancelar` | Cancela una reserva propia (con verificación de propiedad) |

### 5.4 Verificación de propiedad (ownership)

Cuando un usuario de Telegram intenta cancelar una reserva con `/cancelar NOVA-XXXX`, el sistema verifica que esa reserva fue creada desde la misma cuenta:

```python
def comando_cancelar(chat_id: int, codigo: str) -> str:
    sid = _session_id_telegram(chat_id)
    # ...
    if not chatbot_memoria.es_propietario(sid, codigo):
        return "🚫 Acceso denegado: No puedes cancelar esta reserva..."
```

La propiedad se registra automáticamente en `api_telegram.py` cuando se detecta que se creó una reserva exitosamente:

```python
match_codigo = re.search(r"(NOVA-\d{4,})", respuesta)
if match_codigo and "creada" in respuesta.lower():
    chatbot_memoria.registrar_reserva_usuario(sid, match_codigo.group(1))
```

### 5.5 Detección de solapamiento de intervalos

La función `verificar_disponibilidad()` en `almacen_sqlite.py` utiliza la **fórmula estándar de solapamiento de intervalos** para detectar conflictos:

Dados dos intervalos $[I_n, F_n)$ (nuevo) y $[I_e, F_e)$ (existente), existe **solapamiento** si y solo si:

$$I_n < F_e \quad \land \quad F_n > I_e$$

Donde los tiempos se convierten a **minutos desde las 00:00** para la comparación numérica:

$$\text{minutos} = H \times 60 + M$$

**Ejemplo concreto:**

- Reserva existente `NOVA-1001`: Auditorio Nova, 2026-11-15, 09:00–13:00 → $[540, 780)$
- Solicitud nueva: Auditorio Nova, 2026-11-15, 11:00–15:00 → $[660, 900)$
- Verificación: $660 < 780 \land 900 > 540$ → **Verdadero** → ⚠️ **Conflicto detectado**

**Contiguidad permitida:** Si una reserva termina a las 13:00 y otra empieza a las 13:00, **no hay conflicto**: $780 < 780$ es **falso**.

```python
for fila in filas:
    inicio_exist = _a_minutos(fila["hora_inicio"])
    fin_exist = _a_minutos(fila["hora_fin"])
    if inicio_nuevo < fin_exist and fin_nuevo > inicio_exist:
        return {"disponible": False, "motivo": f"Espacio ocupado..."}
```

### 5.6 Validación de horario de operación

Antes de verificar cruces, el sistema valida que el intervalo completo del evento caiga dentro del horario de operación del centro:

$$\text{inicio} \geq 480 \quad (08{:}00) \qquad \land \qquad \text{fin} \leq 1320 \quad (22{:}00)$$

**Ejemplo de rechazo:** Una Recepción de Boda (5 horas) iniciando a las 18:00 terminaría a las 23:00 ($1380 > 1320$) → Rechazada.

### 5.7 Control transaccional (`BEGIN IMMEDIATE`)

Tanto `crear_reserva_db()` como `modificar_reserva_db()` abren transacciones inmediatas para garantizar consistencia:

```python
conn.execute("BEGIN IMMEDIATE")
disp = verificar_disponibilidad(...)
if not disp["disponible"]:
    conn.rollback()
    raise ValueError(disp["motivo"])
# ... INSERT/UPDATE ...
conn.commit()
```

---

## 6. Evolución y Decisiones de Diseño

### 6.1 Cronología de avances

#### Avance 1 — Primera llamada al LLM y extracción estructurada (2026-10-02)

- **Participante:** Santiago Zuluaga
- **Cambio realizado:** Creación del cliente HTTP hacia Groq en Python, pasando el catálogo de NovaEventos en el prompt de sistema.
- **Dificultad encontrada:** El modelo envolvía ocasionalmente el JSON en bloques ` ```json ``` ` o omitía llaves cuando el mensaje era muy corto (ej. `"60 personas"`).
- **Solución:** Se activó `"response_format": {"type": "json_object"}` en el payload de Groq y se implementó la función de extracción local de respaldo con expresiones regulares.

#### Avance 2 — Conversación multi-turno con sesiones (2026-10-09)

- **Participante:** Santiago Zuluaga
- **Cambio realizado:** Implementación de `_sesiones[session_id]` con historial multi-turno y máquina de estados para confirmación, descarte y reinicio.
- **Dificultad encontrada:** Cuando el modelo respondía `null` en campos capturados dos turnos atrás, se borraban del borrador.
- **Solución:** Fusión incremental del borrador — solo se sobreescriben los campos que el nuevo turno aporta con un valor no nulo.

#### Avance 3 — Migración a FastAPI + SQLite (2026-10-15)

- **Participante:** Santiago Zuluaga
- **Cambio realizado:** Reemplazo de `reservas.json` por `almacen_sqlite.py` + `reservas.db`, exposición de reglas de negocio en `main.py` (FastAPI).
- **Dificultad encontrada:** Al modificar una reserva existente (`PUT`), el validador detectaba erróneamente un choque consigo misma.
- **Solución:** Se añadió el parámetro `excluir_codigo` en `verificar_disponibilidad()` → `AND codigo != ?` para ignorar la propia reserva durante reprogramación.

#### Avance 4 — Interfaz Gradio + suite de pruebas (2026-10-21)

- **Participante:** Santiago Zuluaga
- **Cambio realizado:** Construcción de `app_gradio.py` con selector de sesiones, tabla `gr.Dataframe` conectada a SQLite, y `test_sistema_eventos.py`.
- **Dificultad encontrada:** La tabla de reservas no se actualizaba automáticamente tras confirmar desde el chat.
- **Solución:** Todos los callbacks de Gradio devuelven la invocación fresca a `obtener_tabla_reservas()` como salida adicional.

#### Avance 5 — Creación del bot de Telegram (2026-11-05)

- **Participante:** Santiago Zuluaga
- **Cambio realizado:** Creación de `bot_telegram.py` y `api_telegram.py`. Implementación de polling con `python-telegram-bot`, registro de handlers de comandos y conversión de respuestas a MarkdownV2.
- **Dificultad encontrada:** La librería `python-telegram-bot` requiere un manejo asíncrono (`async/await`) de los handlers.
- **Solución:** Se implementaron todos los handlers como funciones `async` y se utilizó `Application.run_polling()` como punto de entrada.

#### Avance 6 — Verificación de propiedad + teclados inline (2026-11-12)

- **Participante:** Santiago Zuluaga
- **Cambio realizado:** Implementación de `chatbot_memoria.py` para gestionar la asociación de reservas por usuario. Creación de `InlineKeyboardMarkup` con botones "✅ Sí, confirmo" y "❌ Cancelar" para la confirmación de reservas.
- **Dificultad encontrada:** El `CallbackQueryHandler` no editaba correctamente el mensaje cuando se pulsaban los botones inline.
- **Solución:** Se usó `query.edit_message_text()` en lugar de `query.message.reply_text()` para actualizar el mensaje original con el resultado de la confirmación o cancelación.

#### Avance 7 — Fallback offline + documentación consolidada (2026-11-19)

- **Participante:** Santiago Zuluaga
- **Cambio realizado:** Creación de `simular_respuesta_perdida.py` para verificar el extractor determinista sin LLM. Redacción de la bitácora consolidada y la matriz de 25 pruebas.
- **Dificultad encontrada:** El script de simulación importaba `consulta_llm` antes de desactivar la API key, provocando que el módulo intentara conectarse.
- **Solución:** Se establece `os.environ["GROQ_API_KEY"] = ""` **antes** de importar `consulta_llm`.

### 6.2 Tabla comparativa: Flowise vs. Gradio vs. Telegram

| Criterio | Primer Corte (Flowise + JSON) | Segundo Corte (Gradio + FastAPI + SQLite) | Tercer Corte (Telegram) |
|:---|:---|:---|:---|
| **Consumo del LLM** | Oculto detrás de bloques visuales de Flowise; sin control del prompt. | Petición HTTP explícita a Groq con `response_format: json_object`, temperatura 0.1. Control total del payload. | Mismo motor (`consulta_llm.py`). Se usa el extractor determinista cuando no hay LLM. |
| **Memoria y Sesiones** | Memoria general del chat, difícil de reiniciar o aislar. | Diccionario `_sesiones[session_id]` con borrador, historial y `esperando_confirmacion`. | Mismas sesiones, con `chat_id` → `tg_{chat_id}`. Se agrega `chatbot_memoria.py` para propiedad de reservas. |
| **Persistencia** | Archivos `.json` planos, propensos a corrupción. | SQLite con transacciones `BEGIN IMMEDIATE`, datos semilla y cancelación lógica. | Misma capa SQLite. Los borradores siguen en RAM. |
| **Reglas de negocio** | Validación básica por texto o coincidencia exacta de hora. | Fórmula de solapamiento de intervalos, validación de horario 08:00–22:00, aforo máximo. | Mismas reglas. Se agrega verificación de propiedad para cancelaciones. |
| **Interfaz de usuario** | Chat embebido genérico en Flowise sin visibilidad de la BD. | App web con chat interactivo, tabla de reservas en vivo, filtros por estado. | Bot en Telegram con comandos nativos, teclados inline y formato MarkdownV2. |
| **Accesibilidad** | Solo en navegador local donde corre Flowise. | Solo en navegador local (puerto 7860). | Disponible desde **cualquier dispositivo** con Telegram instalado. |
| **Código escrito por el equipo** | Nulo (todo visual en Flowise). | ~1,100 líneas de Python (motor + API + UI + tests). | ~1,600 líneas de Python (se agregan bot_telegram, api_telegram, chatbot_memoria, simular_respuesta_perdida). |

---

## 7. Pruebas y Evidencias

### 7.1 Referencia a la Matriz de 25 Pruebas

La documentación completa de las 25 pruebas funcionales se encuentra en la [Matriz de 25 Pruebas](./Matriz_25_Pruebas.md). A continuación se presenta un resumen por grupo:

| Grupo | Pruebas | Descripción |
|:---|:---:|:---|
| **A — Conversación multi-turno** | P01–P05 | Creación de reservas paso a paso, acumulación de slots, mensajes con múltiples datos en un solo turno. |
| **B — Sesiones y aislamiento** | P06–P09 | Dos sesiones simultáneas, reinicio de una sin afectar la otra, sesiones de Telegram vs. Gradio. |
| **C — Validación de disponibilidad** | P10–P14 | Rechazo de cruces horarios, eventos contiguos permitidos, horario fuera de rango, aforo excedido. |
| **D — CRUD completo** | P15–P18 | Crear reserva, consultar por código, modificar horario (`PUT`), cancelar y verificar liberación. |
| **E — Telegram específico** | P19–P22 | Comandos `/start`, `/consultar`, `/cancelar` con propiedad, teclados inline, formato MarkdownV2. |
| **F — Fallback y robustez** | P23–P25 | Simulación offline sin LLM, mensajes inválidos, reinicio del servidor y persistencia. |

### 7.2 Suite de pruebas automatizadas

El archivo `test_sistema_eventos.py` contiene 3 pruebas automatizadas que se ejecutan con `pytest`:

```powershell
.\.venv\Scripts\python.exe -m pytest test_sistema_eventos.py -v
```

| Test | Descripción | Qué verifica |
|:---|:---|:---|
| `test_1_conversacion_varios_turnos_y_creacion` | Envía 4 mensajes en una sesión para crear `NOVA-1004` | Acumulación incremental y creación exitosa |
| `test_2_dos_sesiones_y_reinicio` | Inicia dos sesiones con servicios distintos y reinicia una | Aislamiento de sesiones y limpieza selectiva |
| `test_3_rechazo_intervalos_ocupados_y_cancelacion` | Intenta cruce horario, cancela `NOVA-1001`, reintenta | Validación de cruces, cancelación y liberación |

---

## 8. Fallos y Correcciones

A lo largo del desarrollo se detectaron y corrigieron múltiples problemas. Los 4 más significativos:

### 8.1 JSON envuelto en bloques Markdown por el LLM

- **Problema:** El modelo LLM (Llama 3.3) ocasionalmente respondía envolviendo el JSON en bloques de código Markdown (` ```json ... ``` `), lo cual rompía el parseo de `json.loads()`.
- **Causa raíz:** Sin la directiva `response_format`, el modelo interpreta que debe formatear su respuesta "bonita" para un humano.
- **Corrección:** Se activó `"response_format": {"type": "json_object"}` en el payload enviado a Groq, forzando al modelo a devolver JSON puro sin decoración.
- **Archivo afectado:** `consulta_llm.py`

### 8.2 Auto-conflicto al modificar una reserva (excluir_codigo)

- **Problema:** Al modificar la hora de una reserva existente con `PUT /reservas/{codigo}`, el validador de disponibilidad detectaba erróneamente un conflicto **consigo misma**.
- **Causa raíz:** La consulta SQL `WHERE fecha = ? AND espacio = ? AND estado = 'activa'` incluía la propia reserva en los resultados.
- **Corrección:** Se añadió el parámetro `excluir_codigo` a `verificar_disponibilidad()`:

```python
if excluir_codigo:
    query += " AND codigo != ?"
    params.append(excluir_codigo)
```

- **Archivo afectado:** `almacen_sqlite.py` (función `verificar_disponibilidad`, línea 220)

### 8.3 Pérdida del borrador entre turnos (merge incremental)

- **Problema:** Cuando el LLM respondía `null` para un campo que el usuario ya había proporcionado en un turno anterior, el valor se borraba del borrador.
- **Causa raíz:** La fusión directa sobrescribía todos los campos con los valores del LLM, incluyendo los `null`.
- **Corrección:** Se implementó la fusión incremental: solo se actualizan los campos con valores no nulos. En el extractor determinista:

```python
if m_fecha and (not sesion["fecha"] or "fecha" in texto_lower):
    sesion["fecha"] = m_fecha.group(1)
```

- **Archivo afectado:** `consulta_llm.py`

### 8.4 Escape de caracteres especiales en Telegram MarkdownV2

- **Problema:** Los mensajes enviados al bot de Telegram fallaban con errores de parseo porque caracteres como `.`, `-`, `(`, `)`, `!` no estaban escapados correctamente para MarkdownV2.
- **Causa raíz:** Telegram MarkdownV2 requiere que **todos** los caracteres especiales se escapen con `\`, a diferencia del Markdown estándar.
- **Corrección:** Se creó la función `_escapar_md()` en `api_telegram.py` que escapa exhaustivamente 20 caracteres:

```python
def _escapar_md(texto: str) -> str:
    caracteres = r'_*[]()~`>#+-=|{}.!'
    resultado = ""
    for c in texto:
        if c in caracteres:
            resultado += f"\\{c}"
        else:
            resultado += c
    return resultado
```

Adicionalmente, se creó `formatear_respuesta_telegram()` que preserva las negritas (`**texto**` → `*texto*`) antes de escapar, y luego las reinyecta tras el escapado.

- **Archivo afectado:** `api_telegram.py` (funciones `_escapar_md` y `formatear_respuesta_telegram`)

---

## 9. Limitaciones y Pendientes

| # | Limitación | Descripción | Impacto |
|:---:|:---|:---|:---|
| 1 | **Duración fija por paquete** | Cada servicio tiene una duración predefinida (2, 4 o 5 horas) en `catalogo_eventos.json`. No se pueden reservar fracciones horarias ni combinar paquetes. | Los clientes no pueden personalizar la duración de su evento. |
| 2 | **Sin pasarela de pagos** | El sistema informa los servicios disponibles pero no procesa cobros en línea. | La transacción económica debe realizarse por otros medios (transferencia, efectivo). |
| 3 | **Borradores en RAM** | Los borradores no confirmados y la asociación de propiedad de reservas se almacenan en diccionarios Python en memoria. Se pierden al reiniciar el proceso. | Si el servidor se reinicia, los usuarios no podrán cancelar sus reservas previas vía `/cancelar` (tendrían que solicitarlo a un administrador). |
| 4 | **Sin confirmación por email** | No se envía correo electrónico ni notificación push al usuario tras crear o cancelar una reserva. | El usuario debe guardar manualmente su código `NOVA-XXXX` para futuras consultas. |
| 5 | **Propiedad no persistente** | La relación `session_id` → códigos de reserva vive en RAM (`_reservas_por_usuario`). | Tras reinicio, la verificación de propiedad deja de funcionar para reservas anteriores. |
| 6 | **Sin soporte multi-idioma** | El bot responde exclusivamente en español. | Usuarios de otros idiomas no tienen soporte nativo. |
| 7 | **Sin modificación desde Telegram** | El comando `/cancelar` existe, pero no hay `/modificar` para cambiar la fecha u hora desde Telegram. | Las modificaciones deben hacerse desde la API REST directamente o a través del flujo conversacional. |

---

## 10. Comparación Técnica: Versión Primer Corte (Flowise) vs. Segundo Corte (Gradio) vs. Tercer Corte (Telegram)

| Criterio | Flowise + JSON (1er Corte) | Python + Gradio + FastAPI + SQLite (2do Corte) | Telegram Bot + API (3er Corte) |
|:---|:---|:---|:---|
| **Consumo del LLM** | Oculto en bloques visuales de Flowise. Sin control del prompt, temperatura ni formato de respuesta. | Petición HTTP explícita a Groq: `response_format: json_object`, `temperature: 0.1`. Payload con system prompt dinámico + historial. | Misma infraestructura del 2do corte. Se agrega extractor determinista como fallback completo. |
| **Memoria y Sesiones** | Memoria general del chat; reinicio implica recargar la página completa. | `_sesiones[session_id]` con borrador, historial de mensajes y flag `esperando_confirmacion`. Selector de sesiones en Gradio. | Sesiones por `chat_id` → `tg_{chat_id}`. Se agrega `chatbot_memoria.py` para registrar y verificar propiedad de reservas. |
| **Persistencia de datos** | Archivos `.json` planos en disco. Propensos a corrupción, sin transacciones, sin control de concurrencia. | SQLite (`reservas.db`) con `CREATE TABLE`, transacciones `BEGIN IMMEDIATE`, generación secuencial de códigos `NOVA-XXXX`, datos semilla. | Misma capa SQLite del 2do corte. Los borradores permanecen en RAM. |
| **Reglas de negocio** | Validación básica por coincidencia de texto. Sin cálculo de intervalos. | Fórmula de solapamiento: $I_n < F_e \land F_n > I_e$. Validación de horario 08:00–22:00 y aforo máximo. Parámetro `excluir_codigo`. | Mismas reglas del 2do corte. Se agrega verificación de propiedad (`es_propietario`) para cancelaciones. |
| **Interfaz de usuario** | Chat embebido genérico en la interfaz visual de Flowise. Sin tabla de BD ni inspector de estado. | App web Gradio: chat interactivo + tabla de reservas en vivo + filtros de estado + cancelación por UI. Puerto 7860. | Bot de Telegram: comandos nativos (`/start`, `/consultar`, `/cancelar`), teclados inline, formato MarkdownV2. Accesible desde cualquier dispositivo. |
| **Accesibilidad** | Solo en el navegador local donde se ejecuta Flowise. | Solo en el navegador local (puerto 7860). Requiere que Gradio + FastAPI estén corriendo. | Disponible desde **cualquier dispositivo** con Telegram. Solo requiere que FastAPI y el bot estén activos en el servidor. |
| **Verificación de propiedad** | No implementada. | No implementada (cualquier usuario puede cancelar cualquier reserva desde Gradio). | ✅ Implementada: solo el `chat_id` que creó la reserva puede cancelarla vía `/cancelar`. |
| **Confirmación interactiva** | No implementada. | Botones en Gradio (Confirmar / Descartar / Reiniciar). | Teclados inline de Telegram: "✅ Sí, confirmo" / "❌ Cancelar" con `CallbackQueryHandler`. |
| **Tolerancia a fallos** | Dependencia total del LLM integrado en Flowise. | Extractor de respaldo con regex, pero sin prueba formal de fallback. | Extractor determinista completo + script `simular_respuesta_perdida.py` para verificar funcionamiento sin LLM. |
| **Líneas de código propias** | 0 (configuración visual) | ~1,100 líneas Python | ~1,600 líneas Python (se agregan 4 archivos nuevos) |
| **Pruebas automatizadas** | Ninguna | 3 tests con `pytest` + `TestClient` | 3 tests heredados + script de simulación offline + matriz de 25 pruebas documentadas |

---

## Variables de Entorno del Sistema

Resumen completo de las variables de entorno utilizadas por los distintos módulos del proyecto:

| Variable | Módulo que la usa | Valor por defecto | Descripción |
|:---|:---|:---|:---|
| `GROQ_API_KEY` | `consulta_llm.py` | `""` (vacía) | Token de autenticación para la API de Groq. Si está vacía, se usa el extractor determinista. |
| `GROQ_MODEL` | `consulta_llm.py` | `llama-3.3-70b-versatile` | Nombre del modelo de lenguaje utilizado. |
| `CHATBOT_API_URL` | `consulta_llm.py`, `app_gradio.py` | `http://127.0.0.1:8011` | URL donde corre la API FastAPI. |
| `SQLITE_DB_PATH` | `almacen_sqlite.py` | `reservas.db` (directorio del proyecto) | Ruta del archivo de base de datos SQLite. |
| `TELEGRAM_BOT_TOKEN` | `bot_telegram.py` | `""` (vacía) | Token del bot proporcionado por @BotFather. Requerido para Telegram. |

---

## Instrucciones de Ejecución

### Preparación del entorno

```powershell
# Desde la carpeta raíz NovaEventos/
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### Terminal 1 — API FastAPI (puerto 8011)

```powershell
.\.venv\Scripts\python.exe -m uvicorn main:app --reload --port 8011
```

### Terminal 2 — Bot de Telegram

```powershell
# Configurar variables en .env o como variables de entorno:
# TELEGRAM_BOT_TOKEN=tu_token_de_botfather
# GROQ_API_KEY=tu_clave_de_groq
# CHATBOT_API_URL=http://127.0.0.1:8011

.\.venv\Scripts\python.exe bot_telegram.py
```

### Terminal 2 (alternativa) — Interfaz Gradio (puerto 7860)

```powershell
$env:CHATBOT_API_URL = "http://127.0.0.1:8011"
$env:GROQ_API_KEY = "tu_clave_de_groq"
.\.venv\Scripts\python.exe app_gradio.py
```

### Ejecución de pruebas automatizadas

```powershell
.\.venv\Scripts\python.exe -m pytest test_sistema_eventos.py -v
```

### Simulación de fallback offline

```powershell
.\.venv\Scripts\python.exe simular_respuesta_perdida.py
```

---

## Glosario de Términos

| Término | Definición |
|:---|:---|
| **Borrador** | Diccionario temporal en RAM que acumula los datos parciales de una reserva en construcción antes de la confirmación. |
| **Slot** | Cada campo individual del borrador (servicio, fecha, hora, asistentes, nombre, contacto). |
| **Sesión** | Contexto aislado por usuario, identificado por `session_id` (Gradio) o `tg_{chat_id}` (Telegram). |
| **Solapamiento** | Conflicto temporal entre dos eventos que comparten espacio y tienen intervalos horarios que se cruzan. |
| **Cancelación lógica** | Cambio de `estado` de `'activa'` a `'cancelada'` sin eliminar el registro de la base de datos. |
| **Extractor determinista** | Módulo de procesamiento basado en expresiones regulares que funciona sin conexión al LLM. |
| **Ownership** | Verificación de que el usuario que solicita cancelar una reserva es el mismo que la creó. |
| **InlineKeyboard** | Botones interactivos dentro de un mensaje de Telegram que permiten al usuario confirmar o cancelar acciones. |
| **MarkdownV2** | Formato de texto de Telegram que requiere escapado especial de caracteres para negritas, cursivas, código, etc. |

---

> **Documento generado como parte de la entrega final (tercer corte) de la asignatura Creación de Chatbots con IA — EAM 2026-II.**  
> **Equipo NovaEventos:** Santiago Zuluaga · Jefrey Osorio · Juan Micanquer
