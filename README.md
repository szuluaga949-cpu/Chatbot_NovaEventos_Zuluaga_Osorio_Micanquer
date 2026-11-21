# 🏛️ NovaEventos · Chatbot de Gestión de Reservas (Entrega Final)

Sistema conversacional para la cotización, verificación de disponibilidad, agendamiento, modificación y cancelación de espacios para eventos sociales, empresariales y académicos. El proyecto integra un **bot de Telegram** como interfaz principal, **Python** para el consumo del modelo LLM (Groq), **FastAPI** para la API REST del negocio y **SQLite** (`reservas.db`) para la persistencia transaccional de reservas.

---

## 👥 Identificación e Integrantes

| Campo | Detalle |
| :--- | :--- |
| **Proyecto** | NovaEventos |
| **Asignatura** | Creación de Chatbots con IA · EAM 2026-II |
| **Entrega** | Tercer Corte — Entrega Final |
| **Integrantes** | Santiago Zuluaga, Jefrey Osorio, Juan Micanquer |

**Documentación del proyecto:**
- 📘 [Bitácora Consolidada](./documentacion/Bitacora_Consolidada.md)
- 🧪 [Matriz de 25 Pruebas](./documentacion/Matriz_25_Pruebas.md)
- 📊 [Presentación Final (PDF)](./presentacion/Presentacion_Final.pdf)
- 🖼️ [Carpeta de Evidencias](./evidencias/)

---

## 🎯 Problema y Alcance

### El problema que resuelve

NovaEventos es un centro de convenciones y eventos que administra **cuatro espacios físicos** con reglas estrictas de horario (`08:00` a `22:00`), duración fija por servicio y aforo máximo por salón. Durante la gestión tradicional se presentaban:

1. **Cruces de horarios:** Se agendaban eventos que se pisaban parcialmente en el mismo salón.
2. **Pérdida de contexto:** Si el cliente entregaba datos en varios mensajes, el bot olvidaba la información previa.
3. **Sin confirmación previa:** Las operaciones se ejecutaban sin validación del usuario.
4. **Falta de persistencia:** Al cancelar una reserva se perdía el registro histórico.

### Usuarios del sistema

- **Clientes externos** (organizadores de eventos): Usan el bot de Telegram para consultar, reservar, modificar y cancelar.
- **Coordinadores internos:** Revisan la API de FastAPI (`/docs`) y la tabla de SQLite.

### Funciones implementadas

- ✅ Conversación natural multi-turno recolectando 6 datos obligatorios
- ✅ Múltiples usuarios simultáneos (cada chat de Telegram = sesión independiente)
- ✅ Validación de horario de apertura/cierre, aforo y cruces de intervalos
- ✅ Operaciones CRUD: crear, consultar, modificar y cancelar reservas
- ✅ Verificación de propiedad (solo el creador puede cancelar su reserva)
- ✅ Botones de confirmación inline en Telegram
- ✅ Extractor determinista de respaldo cuando el LLM no responde

### Límites del servicio

- Sin pasarela de pagos en línea
- Duración fija por paquete (no se fraccionan horas sueltas)
- El borrador no confirmado vive en memoria RAM
- Sin envío de comprobante por correo electrónico

---

## 🏗️ Arquitectura

### Recorrido de una solicitud de principio a fin

```
[Usuario en Telegram]
        │
        ▼
[bot_telegram.py] ─── Recibe Update, extrae texto y chat_id
        │
        ▼
[api_telegram.py] ─── Adapta el mensaje y llama al motor conversacional
        │
        ▼
[consulta_llm.py] ─── Gestiona sesión, construye prompt, consulta Groq LLM
        │
        ▼  (Solo cuando el usuario confirma)
[main.py] ─── FastAPI REST API en Puerto 8011
   │── GET    /disponibilidad
   │── POST   /reservas
   │── PUT    /reservas/{codigo}
   └── DELETE /reservas/{codigo}
        │
        ▼
[almacen_sqlite.py] ──→ [reservas.db]
```

### Responsabilidad de cada archivo

| Archivo | Responsabilidad |
| :--- | :--- |
| `bot_telegram.py` | Bot de Telegram: recibe mensajes, enruta comandos, envía respuestas y maneja teclados inline |
| `api_telegram.py` | Adaptador entre Telegram y el motor conversacional; formatea respuestas a MarkdownV2 |
| `consulta_llm.py` | Motor conversacional: sesiones, prompt de sistema, consumo de Groq LLM, extractor de respaldo |
| `chatbot_memoria.py` | Gestión de memoria: sesiones, borradores y asociación de reservas por usuario |
| `main.py` | API REST en FastAPI: endpoints del negocio, validación de esquemas Pydantic |
| `almacen_sqlite.py` | Persistencia SQLite: tabla `reservas`, datos semilla, validación de cruces, transacciones |
| `catalogo_eventos.json` | Catálogo de servicios: 4 eventos con duración, espacio y capacidad |
| `app_gradio.py` | Interfaz web Gradio (conservada del segundo corte) |
| `simular_respuesta_perdida.py` | Prueba de resiliencia sin conexión al LLM |
| `test_sistema_eventos.py` | Suite de pruebas automatizadas con pytest |

---

## ⚙️ Requisitos

- **Python:** 3.11 o superior
- **Sistema operativo:** Windows, macOS o Linux
- **Servicios externos:**
  - Cuenta de [Groq](https://console.groq.com/) con API key (modelo: `llama-3.3-70b-versatile`)
  - Bot de Telegram creado con [@BotFather](https://t.me/BotFather)

---

## 📥 Preparación (desde una copia nueva)

### 1. Clonar el repositorio

```bash
git clone https://github.com/<usuario>/Chatbot_NovaEventos_Zuluaga_Osorio_Micanquer.git
cd Chatbot_NovaEventos_Zuluaga_Osorio_Micanquer
```

### 2. Crear el entorno virtual e instalar dependencias

```powershell
# Windows (PowerShell)
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

```bash
# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## 🔐 Configuración de Variables de Entorno

Copie `.env.example` a `.env` y complete las claves reales:

```powershell
copy .env.example .env
# Edite .env con sus claves reales
```

| Variable | Descripción | Proceso que la usa | Valor por defecto |
| :--- | :--- | :--- | :--- |
| `GROQ_API_KEY` | Clave de API de Groq para consultar el LLM | `consulta_llm.py` | *(Requerida)* |
| `GROQ_MODEL` | Modelo de lenguaje utilizado | `consulta_llm.py` | `llama-3.3-70b-versatile` |
| `CHATBOT_API_URL` | Dirección local donde corre FastAPI | `consulta_llm.py`, `api_telegram.py` | `http://127.0.0.1:8011` |
| `SQLITE_DB_PATH` | Ruta del archivo de base de datos SQLite | `almacen_sqlite.py` | `reservas.db` |
| `TELEGRAM_BOT_TOKEN` | Token del bot proporcionado por @BotFather | `bot_telegram.py` | *(Requerida)* |

> ⚠️ **IMPORTANTE:** Las claves, tokens y contraseñas **no se suben al repositorio**. El archivo `.env` está excluido por `.gitignore`.

---

## 🚀 Arranque: Iniciar FastAPI y el Bot de Telegram

La aplicación necesita **dos terminales** ejecutándose simultáneamente.

### Terminal 1 · Iniciar la API del negocio (FastAPI)

Desde la carpeta raíz del proyecto:

```powershell
.\.venv\Scripts\python.exe -m uvicorn main:app --reload --port 8011
```

- **Verificar:** Abrir `http://127.0.0.1:8011/docs` → Swagger UI debe cargar correctamente.
- La base de datos `reservas.db` se crea automáticamente con 3 reservas de prueba.

### Terminal 2 · Iniciar el bot de Telegram

Abrir una **segunda terminal** en la carpeta raíz:

```powershell
.\.venv\Scripts\python.exe bot_telegram.py
```

- **Verificar:** En la terminal debe aparecer `Iniciando bot de Telegram NovaEventos...`
- El bot responde inmediatamente a mensajes en Telegram.

### Alternativa rápida (Windows)

```powershell
.\scripts_windows\iniciar.bat
```

---

## 💬 Uso del Chatbot en Telegram

### Enlace público del bot

Busca `@NovaEventosBot` en Telegram (o usa el enlace directo proporcionado por el equipo).

> **Nota:** Para que el bot responda, los procesos de FastAPI y `bot_telegram.py` deben estar en ejecución.

### Comandos disponibles

| Comando | Función |
| :--- | :--- |
| `/start` | Bienvenida y reinicio de conversación |
| `/ayuda` | Ayuda completa con lista de comandos |
| `/reiniciar` | Limpiar la sesión actual (conserva reservas en DB) |
| `/reservas` | Ver reservas creadas desde esta cuenta |
| `/todas` | Ver todas las reservas activas del sistema |
| `/consultar NOVA-XXXX` | Ver detalles de una reserva específica |
| `/cancelar NOVA-XXXX` | Cancelar una reserva propia |

### Ejemplo de conversación para reservar

```
👤 Usuario: Quiero reservar una Conferencia Corporativa para el 2026-12-01
🤖 Bot:     Perfecto, servicio seleccionado (EVT-CORP). ¿A qué hora deseas iniciar?

👤 Usuario: A las 10:00 para 60 personas
🤖 Bot:     Perfecto. Por favor, indícame tu nombre completo y tu contacto.

👤 Usuario: Santiago Zuluaga, 3005551122
🤖 Bot:     ¿Confirmas los datos de tu reserva?
            - Servicio: Conferencia Corporativa (Auditorio Nova)
            - Fecha: 2026-12-01
            - Hora: 10:00
            - Asistentes: 60
            - Cliente: Santiago Zuluaga (3005551122)
            [✅ Sí, confirmo]  [❌ Cancelar]

👤 Usuario: (presiona ✅ Sí, confirmo)
🤖 Bot:     ¡Reserva creada con éxito! Tu código: NOVA-1004. Espacio: Auditorio Nova.
```

---

## 🗄️ Datos y Navegación

### Catálogo del negocio (`catalogo_eventos.json`)

| ID | Servicio | Espacio | Duración | Capacidad Máxima |
| :--- | :--- | :--- | :---: | :---: |
| `EVT-CORP` | Conferencia Corporativa | Auditorio Nova | 4 horas | 100 personas |
| `EVT-BODA` | Recepción de Boda / Gala Social | Salón Imperial | 5 horas | 200 personas |
| `EVT-CUMP` | Celebración de Cumpleaños | Salón Social | 4 horas | 80 personas |
| `EVT-WORK` | Taller Ejecutivo / Workshop | Sala Innovación | 2 horas | 30 personas |

### Base de datos SQLite (`reservas.db`)

La base de datos se genera automáticamente al iniciar `main.py` en la carpeta raíz del proyecto. Si la tabla `reservas` está vacía, se insertan 3 reservas ficticias de prueba (`NOVA-1001`, `NOVA-1002` activas y `NOVA-1003` cancelada).

**Esquema de la tabla:**
```sql
CREATE TABLE IF NOT EXISTS reservas (
    codigo TEXT PRIMARY KEY,           -- NOVA-XXXX (generado automáticamente)
    cliente_nombre TEXT NOT NULL,
    cliente_contacto TEXT NOT NULL,
    servicio_id TEXT NOT NULL,          -- EVT-CORP, EVT-BODA, etc.
    servicio_nombre TEXT NOT NULL,
    espacio TEXT NOT NULL,
    fecha TEXT NOT NULL,                -- YYYY-MM-DD
    hora_inicio TEXT NOT NULL,          -- HH:MM
    duracion_horas INTEGER NOT NULL,
    hora_fin TEXT NOT NULL,             -- HH:MM (calculada automáticamente)
    asistentes INTEGER NOT NULL,
    estado TEXT NOT NULL,               -- 'activa' o 'cancelada'
    notas TEXT DEFAULT '',
    creado_en TEXT NOT NULL,
    actualizado_en TEXT NOT NULL
);
```

### Documentación del proyecto

| Documento | Ruta |
| :--- | :--- |
| Bitácora Consolidada | [`documentacion/Bitacora_Consolidada.md`](./documentacion/Bitacora_Consolidada.md) |
| Matriz de 25 Pruebas | [`documentacion/Matriz_25_Pruebas.md`](./documentacion/Matriz_25_Pruebas.md) |
| Presentación Final | [`presentacion/Presentacion_Final.pdf`](./presentacion/Presentacion_Final.pdf) |
| Evidencias de pruebas | [`evidencias/`](./evidencias/) |

---

## 📂 Estructura del Repositorio

```text
Chatbot_NovaEventos_Zuluaga_Osorio_Micanquer/
├── README.md                         # Este archivo: guía completa del proyecto
├── requirements.txt                  # Dependencias de Python
├── .gitignore                        # Archivos excluidos del repositorio
├── .env.example                      # Plantilla de variables de entorno
│
├── main.py                           # API REST de negocio en FastAPI (Puerto 8011)
├── bot_telegram.py                   # Bot de Telegram (polling)
├── api_telegram.py                   # Adaptador Telegram ↔ motor conversacional
├── consulta_llm.py                   # Motor conversacional + consumo LLM Groq
├── chatbot_memoria.py                # Gestión de memoria y sesiones
├── almacen_sqlite.py                 # Persistencia SQLite y reglas de negocio
├── catalogo_eventos.json             # Catálogo de servicios del negocio
├── app_gradio.py                     # Interfaz web Gradio (segundo corte)
├── simular_respuesta_perdida.py      # Prueba de resiliencia sin LLM
├── test_sistema_eventos.py           # Suite de pruebas automatizadas (pytest)
│
├── documentacion/
│   ├── Bitacora_Consolidada.md       # Documentación principal del proyecto
│   └── Matriz_25_Pruebas.md         # 25 casos de prueba con evidencias
│
├── evidencias/
│   └── T01_servicios.png ... T25_*.png  # Capturas de pantalla de pruebas
│
├── presentacion/
│   └── Presentacion_Final.pdf        # Presentación ejecutiva del proyecto
│
├── prompts/
│   ├── slot_extractor.txt            # Prompt de extracción de entidades
│   └── system_concierge.txt          # Prompt del concierge NovaConcierge
│
└── scripts_windows/
    ├── iniciar.bat                   # Lanzador de las dos terminales
    └── instalar.bat                  # Instalación desde cero
```

---

## ✅ Comprobación Inicial y Errores Frecuentes

### Prueba rápida paso a paso
1. Inicie FastAPI en Terminal 1 y el bot en Terminal 2.
2. En Telegram, envíe `/start` al bot.
3. Escriba: `Quiero reservar una Conferencia Corporativa para el 2026-11-15 a las 11:00 para 50 personas`
4. **Resultado esperado:** El bot rechazará la reserva indicando que el `Auditorio Nova` ya está ocupado de `09:00` a `13:00` por la reserva activa `NOVA-1001`.
5. Escriba: `Cambia la hora a las 14:00` y confirme.
6. **Resultado esperado:** Se guarda la reserva `NOVA-1004` de `14:00` a `18:00`.

### Ejecución de pruebas automatizadas
```powershell
.\.venv\Scripts\python.exe -m pytest test_sistema_eventos.py -v
```

### Errores frecuentes y solución
| Error | Solución |
| :--- | :--- |
| `No se encontró TELEGRAM_BOT_TOKEN` | Configure el token en `.env` o como variable de entorno |
| `No fue posible conectar con FastAPI en http://127.0.0.1:8011` | Verifique que Terminal 1 con `uvicorn` esté encendida |
| `Intervalo fuera del horario de atención` | El centro opera de 08:00 a 22:00; ajuste la hora de inicio |
| `Conflict: terminated by other getUpdates` | Cierre otras instancias del bot que estén corriendo |
