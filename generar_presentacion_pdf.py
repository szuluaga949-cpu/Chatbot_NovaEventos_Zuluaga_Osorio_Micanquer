"""Generador de la Presentación Final en PDF para NovaEventos (Tercer Corte).

Genera un documento PDF multipágina de alta calidad (1600x900 px por slide)
en `presentacion/Presentacion_Final.pdf` que explica el proyecto de manera
comprensible para cualquier persona que no haya visto el curso.
"""

from pathlib import Path
import textwrap
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = Path(__file__).resolve().parent
PRES_DIR = BASE_DIR / "presentacion"
PRES_DIR.mkdir(parents=True, exist_ok=True)
PDF_PATH = PRES_DIR / "Presentacion_Final.pdf"

# Paleta de diseño profesional (EAM / NovaEventos)
NAVY = (16, 42, 76)
BLUE = (0, 119, 182)
CYAN_BG = (227, 244, 250)
CYAN_BORDER = (29, 169, 202)
BG_SLIDE = (248, 251, 253)
WHITE = (255, 255, 255)
CODE_BG = (16, 35, 63)
CODE_FG = (242, 247, 255)
BORDER_GRAY = (203, 220, 232)
MUTED = (100, 118, 139)
GREEN = (39, 174, 96)


def cargar_fuente(tipo: str, tamano: int):
    rutas_windows = {
        "regular": ["C:/Windows/Fonts/segoeui.ttf", "C:/Windows/Fonts/arial.ttf"],
        "bold": ["C:/Windows/Fonts/segoeuib.ttf", "C:/Windows/Fonts/arialbd.ttf"],
        "mono": ["C:/Windows/Fonts/consola.ttf", "C:/Windows/Fonts/cour.ttf"],
    }
    for ruta in rutas_windows.get(tipo, []):
        if Path(ruta).exists():
            try:
                return ImageFont.truetype(ruta, tamano)
            except Exception:
                pass
    return ImageFont.load_default()


F_EYEBROW = cargar_fuente("bold", 18)
F_H1 = cargar_fuente("bold", 44)
F_H2 = cargar_fuente("bold", 34)
F_H3 = cargar_fuente("bold", 23)
F_LEAD = cargar_fuente("regular", 23)
F_BODY = cargar_fuente("regular", 19)
F_BOLD = cargar_fuente("bold", 19)
F_SMALL = cargar_fuente("regular", 17)
F_CODE = cargar_fuente("mono", 16)


def base_slide(eyebrow: str, titulo: str, num_pag: int, total_pag: int = 9):
    img = Image.new("RGB", (1600, 900), color=BG_SLIDE)
    draw = ImageDraw.Draw(img)
    draw.rectangle([(0, 0), (1600, 10)], fill=BLUE)
    draw.text((70, 38), eyebrow.upper(), fill=BLUE, font=F_EYEBROW)
    draw.text((70, 68), titulo, fill=NAVY, font=F_H2 if num_pag > 1 else F_H1)
    draw.text((1460, 848), f"{num_pag} / {total_pag}", fill=MUTED, font=F_SMALL)
    return img, draw


def dibujar_parrafo(draw, texto: str, x: int, y: int, ancho_chars: int, fuente=F_BODY, color=NAVY, interlineado: int = 28) -> int:
    for linea in textwrap.wrap(texto, width=ancho_chars):
        draw.text((x, y), linea, fill=color, font=fuente)
        y += interlineado
    return y


def dibujar_lista(draw, items: list, x: int, y: int, ancho_chars: int) -> int:
    for item in items:
        lineas = textwrap.wrap(item, width=ancho_chars)
        for i, linea in enumerate(lineas):
            prefijo = "•  " if i == 0 else "    "
            draw.text((x, y), prefijo + linea, fill=NAVY, font=F_BODY)
            y += 28
        y += 8
    return y


def dibujar_nota(draw, texto: str, x: int, y: int, w: int = 1460) -> int:
    lineas = textwrap.wrap(texto, width=int(w / 11.2))
    h = max(64, len(lineas) * 26 + 26)
    draw.rectangle([(x, y), (x + w, y + h)], fill=CYAN_BG)
    draw.rectangle([(x, y), (x + 6, y + h)], fill=CYAN_BORDER)
    ty = y + 12
    for l in lineas:
        draw.text((x + 22, ty), l, fill=NAVY, font=F_BODY)
        ty += 26
    return y + h + 14


def dibujar_tabla(draw, headers: list, filas: list, x: int, y: int, col_widths: list) -> int:
    total_w = sum(col_widths)
    draw.rectangle([(x, y), (x + total_w, y + 44)], fill=(235, 246, 252), outline=BORDER_GRAY)
    cx = x
    for h_txt, w in zip(headers, col_widths):
        draw.text((cx + 12, y + 10), h_txt, fill=BLUE, font=F_BOLD)
        cx += w
    y += 44

    for fila in filas:
        max_lines = 1
        celdas_envueltas = []
        for celda, w in zip(fila, col_widths):
            lineas = textwrap.wrap(str(celda), width=max(10, int((w - 22) / 10.2)))
            celdas_envueltas.append(lineas)
            max_lines = max(max_lines, len(lineas))
        row_h = max_lines * 25 + 18
        draw.rectangle([(x, y), (x + total_w, y + row_h)], fill=WHITE, outline=BORDER_GRAY)
        cx = x
        for lineas, w in zip(celdas_envueltas, col_widths):
            ty = y + 9
            for l in lineas:
                draw.text((cx + 12, ty), l, fill=NAVY, font=F_SMALL)
                ty += 25
            cx += w
        y += row_h
    return y + 14


def generar_presentacion():
    slides = []

    # SLIDE 1: Portada e Identificación
    img, d = base_slide("EAM 2026-II · Creación de Chatbots con IA · Entrega Final", "NovaEventos: Chatbot de Reservas en Telegram con FastAPI y SQLite", 1)
    dibujar_parrafo(
        d,
        "Solución conversacional completa para la cotización, verificación de disponibilidad horaria, agendamiento, modificación y cancelación de eventos sociales y corporativos.",
        70, 140, 115, fuente=F_LEAD
    )
    # Tarjeta Izquierda: Integrantes y Datos
    d.rectangle([(70, 225), (780, 660)], fill=WHITE, outline=BORDER_GRAY, width=2)
    d.text((95, 250), "1. Identificación del Equipo y Proyecto", fill=BLUE, font=F_H3)
    dibujar_lista(d, [
        "Proyecto: NovaEventos (Versión 3.0 — Entrega Final Tercer Corte).",
        "Integrantes: Santiago Zuluaga, Jefrey Osorio, Juan Micanquer.",
        "Canal principal: Bot de Telegram interactivo con InlineKeyboards.",
        "Motor conversacional: Python con LLM Groq (llama-3.3-70b-versatile).",
        "API del negocio: FastAPI (puerto 8011) con endpoints REST.",
        "Persistencia: SQLite relacional transaccional (reservas.db).",
        "Repositorio oficial: Chatbot_NovaEventos_Zuluaga_Osorio_Micanquer.",
    ], 95, 295, 58)
    # Tarjeta Derecha: Necesidad Atendida
    d.rectangle([(815, 225), (1530, 660)], fill=WHITE, outline=BORDER_GRAY, width=2)
    d.text((840, 250), "2. El Negocio y el Problema que Resuelve", fill=BLUE, font=F_H3)
    dibujar_lista(d, [
        "Centro de Convenciones NovaEventos: 4 espacios especializados con horarios estrictos (08:00 a 22:00) y duración por paquete.",
        "Problemas tradicionales: Cruces de reservas, clientes que dan datos por partes y se pierde el contexto, cancelaciones sin control.",
        "Solución implementada: Validación matemática de intervalos en minutos, memoria de sesión multi-turno y verificación de propiedad.",
    ], 840, 295, 58)
    dibujar_nota(d, "Diseñado para sustentación comprensible: Cualquier persona sin conocimientos previos del curso puede entender la necesidad, la solución y los resultados.", 70, 690)
    slides.append(img)

    # SLIDE 2: Problema, Usuarios y Alcance
    img, d = base_slide("1. Solución y Alcance", "Catálogo de Espacios, Usuarios, Funciones y Límites", 2)
    dibujar_parrafo(d, "Usuarios: Clientes organizadores de eventos (vía Telegram) y administradores/coordinadores (vía FastAPI /docs y SQLite). Horario de atención: 08:00 a 22:00 todos los días.", 70, 125, 120)
    y = dibujar_tabla(
        d,
        ["ID Servicio", "Servicio / Evento", "Espacio Físico", "Duración", "Aforo Máx.", "Reglas Clave"],
        [
            ["EVT-CORP", "Conferencia Corporativa", "Auditorio Nova", "4 horas", "100 pers.", "Sonido pro, microfonía, pantalla 4K"],
            ["EVT-BODA", "Recepción de Boda / Gala Social", "Salón Imperial", "5 horas", "200 pers.", "Montaje de gala, pista LED, suite nupcial"],
            ["EVT-CUMP", "Celebración de Cumpleaños", "Salón Social", "4 horas", "80 pers.", "Mobiliario lounge, barra y sonido"],
            ["EVT-WORK", "Taller Ejecutivo / Workshop", "Sala Innovación", "2 horas", "30 pers.", "Mesas modulares, proyector, pizarras"],
        ],
        70, 200, [150, 390, 260, 160, 160, 340]
    )
    dibujar_nota(d, "Alcance implementado: Multi-turno, sesiones aisladas, validación de cruces en SQLite, comandos /consultar y /cancelar con propiedad de usuario. Límites: Sin cobro en línea ni fraccionamiento fuera de paquete.", 70, y + 15)
    slides.append(img)

    # SLIDE 3: Arquitectura y Recorrido de una Solicitud
    img, d = base_slide("2. Arquitectura del Sistema", "Recorrido Técnico de una Solicitud: Telegram → Python → FastAPI → SQLite", 3)
    d.rectangle([(70, 135), (780, 690)], fill=WHITE, outline=BORDER_GRAY, width=2)
    d.text((95, 160), "Responsabilidad de cada Módulo", fill=BLUE, font=F_H3)
    dibujar_lista(d, [
        "bot_telegram.py: Recibe Updates vía polling, administra comandos (/start, /reservas, /consultar, /cancelar) y botones inline.",
        "api_telegram.py: Adaptador que enruta a consulta_llm y convierte respuestas a MarkdownV2 con escapado seguro.",
        "consulta_llm.py: Motor de conversación, conexión a Groq LLM (Llama 3.3) y extractor determinista de respaldo sin red.",
        "chatbot_memoria.py: Aísla borradores por tg_{chat_id} y asocia reservas para verificación de propiedad.",
        "main.py: API REST FastAPI con validación Pydantic.",
        "almacen_sqlite.py: Persistencia transaccional en reservas.db.",
    ], 95, 205, 58)

    d.rectangle([(810, 135), (1530, 690)], fill=CODE_BG, outline=BORDER_GRAY, width=2)
    d.text((835, 160), "Flujo Arquitectónico de una Petición", fill=(102, 217, 239), font=F_H3)
    flujo_ascii = (
        "[Usuario en Telegram (App Celular / PC)]\n"
        "                   │\n"
        "                   ▼ (HTTPS Polling)\n"
        "[bot_telegram.py] ── InlineKeyboard Confirm/Cancel\n"
        "                   │\n"
        "                   ▼\n"
        "[api_telegram.py] ── Adaptador de sesión y formato\n"
        "                   │\n"
        "                   ▼\n"
        "[consulta_llm.py] ── Groq LLM / Fallback Regex\n"
        "   └── Guarda borrador en [chatbot_memoria.py]\n"
        "                   │\n"
        "                   ▼ (Solo tras confirmación explícita)\n"
        "[main.py] (FastAPI REST API Puerto 8011)\n"
        "   ├── GET  /disponibilidad\n"
        "   ├── POST /reservas (HTTP 201 / 409)\n"
        "   ├── PUT  /reservas/{codigo}\n"
        "   └── DELETE /reservas/{codigo}\n"
        "                   │\n"
        "                   ▼\n"
        "[almacen_sqlite.py] ──> [reservas.db (SQLite)]"
    )
    ty = 210
    for l in flujo_ascii.splitlines():
        d.text((835, ty), l, fill=CODE_FG, font=F_CODE)
        ty += 23
    dibujar_nota(d, "Seguridad y separación estricta: El bot de Telegram nunca escribe directamente en SQLite; toda transacción pasa por las reglas de negocio de FastAPI.", 70, 715)
    slides.append(img)

    # SLIDE 4: Recorrido de Uso Paso a Paso
    img, d = base_slide("3. Recorrido de Uso del Chatbot", "Demostración de Conversación Multi-Turno, Confirmación y Registro Real", 4)
    d.rectangle([(70, 135), (780, 675)], fill=WHITE, outline=BORDER_GRAY, width=2)
    d.text((95, 160), "Paso a Paso en Telegram", fill=BLUE, font=F_H3)
    dibujar_lista(d, [
        "1. Turno 1 (Servicio y Fecha): Cliente escribe 'Quiero una conferencia para el 2026-12-05'. El bot extrae EVT-CORP y fecha.",
        "2. Turno 2 (Hora y Aforo): 'A las 09:00 para 80 personas'. El bot acumula slots y valida aforo (80 <= 100 max).",
        "3. Turno 3 (Identificación): 'Santiago Zuluaga, 3001234567'. Se arma el borrador completo y muestra resumen.",
        "4. Turno 4 (Confirmación): Botón inline 'Sí, confirmo'. Se despacha POST /reservas a FastAPI.",
        "5. Resultado: Código NOVA-1004 asignado en Auditorio Nova de 09:00 a 13:00 con registro permanente en SQLite.",
    ], 95, 205, 58)

    d.rectangle([(810, 135), (1530, 675)], fill=WHITE, outline=BORDER_GRAY, width=2)
    d.text((835, 160), "Fila Generada en SQLite (reservas.db)", fill=BLUE, font=F_H3)
    dibujar_lista(d, [
        "codigo: NOVA-1004 (secuencial autoincremental)",
        "cliente_nombre: Santiago Zuluaga",
        "cliente_contacto: 3001234567",
        "servicio_id: EVT-CORP",
        "servicio_nombre: Conferencia Corporativa",
        "espacio: Auditorio Nova",
        "fecha: 2026-12-05",
        "hora_inicio: 09:00 | duracion_horas: 4 | hora_fin: 13:00",
        "asistentes: 80 | estado: activa",
        "creado_en: 2026-11-21T11:45:00",
    ], 835, 205, 58)
    dibujar_nota(d, "El cliente puede usar /consultar NOVA-1004 para verificar su estado o /cancelar NOVA-1004 para liberar el salón inmediatamente.", 70, 700)
    slides.append(img)

    # SLIDE 5: Reglas del Negocio y Validación Matemática
    img, d = base_slide("4. Reglas del Negocio y Disponibilidad", "Cálculo en Minutos, Horario de Atención y Prevención de Cruces", 5)
    d.rectangle([(70, 135), (780, 690)], fill=WHITE, outline=BORDER_GRAY, width=2)
    d.text((95, 160), "Validaciones del Motor de Reservas", fill=BLUE, font=F_H3)
    dibujar_lista(d, [
        "1. Duración fija por catálogo: hora_fin = hora_inicio + (duracion_horas * 60 minutos). El usuario nunca inventa la hora de fin.",
        "2. Horario estricto (08:00 a 22:00): Todo el intervalo [inicio, fin) debe quedar dentro del horario. Boda a las 19:00 termina 24:00 → Rechazada.",
        "3. Límite de aforo: Si asistentes > capacidad_maxima del espacio → Rechazado antes de tocar base de datos.",
        "4. Control de concurrencia: Transacciones BEGIN IMMEDIATE en SQLite para evitar condiciones de carrera.",
    ], 95, 205, 58)

    d.rectangle([(810, 135), (1530, 690)], fill=CODE_BG, outline=BORDER_GRAY, width=2)
    d.text((835, 160), "Algoritmo de Prevención de Cruces", fill=(102, 217, 239), font=F_H3)
    algo_code = (
        "# Condición matemática de solapamiento entre intervalos:\n"
        "# [inicio_nuevo, fin_nuevo) vs [inicio_exist, fin_exist)\n\n"
        "SELECT codigo, hora_inicio, hora_fin\n"
        "FROM reservas\n"
        "WHERE fecha = ? AND espacio = ? AND estado = 'activa'\n"
        "  AND codigo != ?;  -- Excluye propia al modificar\n\n"
        "for fila in filas:\n"
        "    if (inicio_nuevo < fin_exist and\n"
        "        fin_nuevo > inicio_exist):\n"
        "        raise HTTPException(status_code=409, detail=(\n"
        "            f'El espacio {espacio} ya está ocupado '\n"
        "            f'de {fila[\"hora_inicio\"]} a {fila[\"hora_fin\"]} '\n"
        "            f'(Reserva activa {fila[\"codigo\"]}).'\n"
        "        ))"
    )
    ty = 210
    for l in algo_code.splitlines():
        d.text((835, ty), l, fill=CODE_FG, font=F_CODE)
        ty += 23
    dibujar_nota(d, "Cancelación lógica: Al cancelar, estado pasa a 'cancelada'; la fila se conserva para auditoría y el espacio se libera al instante.", 70, 715)
    slides.append(img)

    # SLIDE 6: Evolución del Proyecto en los Tres Cortes
    img, d = base_slide("5. Evolución del Proyecto", "Comparación Técnica Integral: Primer Corte vs. Segundo Corte vs. Tercer Corte", 6)
    y = dibujar_tabla(
        d,
        ["Dimensión", "Corte 1 (Flowise + JSON)", "Corte 2 (Python + Gradio)", "Corte 3 (Telegram + FastAPI + SQLite)"],
        [
            ["Interfaz", "Chat embebido de Flowise", "Web Gradio (puerto 7860)", "Bot de Telegram interactivo con InlineKeyboards"],
            ["LLM", "Caja negra en nodo visual", "Petición HTTP a Groq en Python", "Groq LLM + Extractor determinista fallback offline"],
            ["Sesiones", "Memoria efímera compartida", "SESIONES[session_id] en RAM", "Aislamiento por chat_id y control de propiedad"],
            ["Persistencia", "Archivo reservas.json plano", "SQLite relacional (reservas.db)", "SQLite transaccional con BEGIN IMMEDIATE"],
            ["Disponibilidad", "Validación textual simple", "Intervalos matemáticos en minutos", "Cruce estricto + /todas + /consultar + /cancelar"],
            ["Resiliencia", "Falla si cae Flowise", "Falla si cae Groq API", "simular_respuesta_perdida.py valida modo offline"],
        ],
        70, 140, [190, 390, 410, 470]
    )
    dibujar_nota(d, "Evolución técnica real: De prototipo sin código en Flowise a un sistema cliente-servidor robusto, testeado y desplegado en Telegram.", 70, y + 10)
    slides.append(img)

    # SLIDE 7: Matriz de 25 Pruebas y Resultados
    img, d = base_slide("6. Matriz de 25 Pruebas y Evidencias", "Verificación Exhaustiva en 6 Grupos según Guía de Evaluación", 7)
    y = dibujar_tabla(
        d,
        ["Grupo de Pruebas", "Cant.", "Objetivo Evaluado", "Comportamiento Verificado", "Estado"],
        [
            ["1. Conversaciones normales", "6", "Consultas, precios, flujos 1-turno y multi-turno", "Respuestas correctas, acumulación y registro SQLite", "6/6 OK"],
            ["2. Preguntas ambiguas", "4", "Sin servicio, fechas relativas, datos incompletos", "El bot repregunta exactamente el dato faltante", "4/4 OK"],
            ["3. Contexto y memoria", "4", "2 cuentas, /reiniciar, cambio de datos, doble click", "Aislamiento de sesiones y protección de botones", "4/4 OK"],
            ["4. Fuera del dominio", "3", "Preguntas ajenas, inyección SQL, mensajes emojis", "Reencause amigable y consultas SQL parametrizadas", "3/3 OK"],
            ["5. Operaciones de negocio", "5", "Crear, consultar, cancelar, cruce, acceso ajeno", "Registro en BD, liberación de horario y ownership", "5/5 OK"],
            ["6. Errores y límites", "3", "Fuera de horario (22:00), sobrecupo, código falso", "Alerta clara de la regla violada y reintento fácil", "3/3 OK"],
        ],
        70, 140, [280, 70, 480, 500, 130]
    )
    dibujar_nota(d, "Total: 25/25 pruebas aprobadas con éxito. Cada caso cuenta con captura oficial en evidencias/ (T01 a T25) enlazada en la matriz.", 70, y + 15)
    slides.append(img)

    # SLIDE 8: Fallos Encontrados y Correcciones Aplicadas
    img, d = base_slide("7. Fallos y Correcciones de Ingeniería", "Problemas Reales Detectados durante el Desarrollo y Soluciones Implementadas", 8)
    y = dibujar_tabla(
        d,
        ["Caso / Fallo", "Causa Raíz", "Corrección Aplicada en Código", "Resultado Verificado"],
        [
            ["Formato JSON de Groq", "El LLM a veces envolvía respuesta en ```json o texto.", "Se activó response_format json_object y extractor regex.", "Extracción 100% estable incluso sin conexión."],
            ["Conflicto al modificar", "Al cambiar hora con PUT, detectaba cruce consigo misma.", "Parámetro excluir_codigo en verificar_disponibilidad().", "Reprogramaciones fluidas sin falsos positivos."],
            ["Pérdida de slots", "Si el usuario decía solo la hora, el bot olvidaba la fecha.", "Fusión incremental que solo sobreescribe valores no nulos.", "Multi-turno retiene contexto de principio a fin."],
            ["MarkdownV2 en Telegram", "Caracteres como '-', '.', '!' rompían el parser de Telegram.", "Función _escapar_md() en api_telegram.py.", "Mensajes con formato profesional sin errores 400."],
            ["Cancelación no autorizada", "Cualquier usuario podía cancelar reservas de otros.", "chatbot_memoria.py valida ownership (es_propietario).", "Rechazo seguro con aviso de 'Acceso denegado'."],
        ],
        70, 140, [260, 390, 470, 340]
    )
    dibujar_nota(d, "Metodología rigurosa: Cada corrección fue verificada repitiendo las pruebas afectadas y ejecutando test_sistema_eventos.py.", 70, y + 15)
    slides.append(img)

    # SLIDE 9: Sustentación, Checklist de Entrega y Cierre
    img, d = base_slide("8. Sustentación y Checklist de Entrega", "Puntos Clave para la Demostración en Vivo y Repositorio Final", 9)
    d.rectangle([(70, 135), (780, 675)], fill=WHITE, outline=BORDER_GRAY, width=2)
    d.text((95, 160), "Guion para la Sustentación del Lunes", fill=BLUE, font=F_H3)
    dibujar_lista(d, [
        "1. Demostración con 2 cuentas: Cuenta A reserva Conferencia (Auditorio Nova) y Cuenta B reserva Taller (Sala Innovación).",
        "2. Consulta y modificación: Cuenta A consulta /consultar y reprograma su evento a otro horario.",
        "3. Prueba de cruce: Intentar reservar Auditorio Nova en horario ocupado → Mostrar rechazo 409.",
        "4. Prueba de seguridad: Cuenta B intenta /cancelar reserva de Cuenta A → Mostrar 'Acceso denegado'.",
        "5. Liberación: Cuenta A cancela su reserva → Inmediatamente el horario queda disponible para Cuenta B.",
        "6. Persistencia: Reiniciar servidores y demostrar que reservas.db mantiene los datos intactos.",
    ], 95, 205, 58)

    d.rectangle([(810, 135), (1530, 675)], fill=WHITE, outline=BORDER_GRAY, width=2)
    d.text((835, 160), "Checklist de los 5 Entregables", fill=BLUE, font=F_H3)
    dibujar_lista(d, [
        "✅ 1. Proyecto completo y funcional (Telegram + FastAPI + SQLite).",
        "✅ 2. README completo con instrucciones paso a paso.",
        "✅ 3. Bitácora consolidada en documentacion/Bitacora_Consolidada.md.",
        "✅ 4. Matriz de 25 pruebas con evidencias en documentacion/.",
        "✅ 5. Presentación ejecutiva en presentacion/Presentacion_Final.pdf.",
        "✅ Repositorio público: Chatbot_NovaEventos_Zuluaga_Osorio_Micanquer.",
        "✅ Credenciales y .env excluidos correctamente en .gitignore.",
    ], 835, 205, 58)
    dibujar_nota(d, "Equipo NovaEventos: Santiago Zuluaga, Jefrey Osorio, Juan Micanquer. Proyecto listo para sustentación y evaluación final.", 70, 700)
    slides.append(img)

    # Guardar PDF multipágina
    slides[0].save(
        PDF_PATH,
        "PDF",
        resolution=150.0,
        save_all=True,
        append_images=slides[1:],
    )
    print(f"\n[FINALIZADO] Presentación de {len(slides)} slides generada exitosamente en:\n{PDF_PATH}")


if __name__ == "__main__":
    generar_presentacion()
