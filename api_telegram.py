"""Adaptador entre el bot de Telegram y el motor conversacional de NovaEventos.

Recibe los mensajes y comandos del usuario de Telegram, los enruta al motor
de conversación (consulta_llm.py) y formatea las respuestas para Telegram.
También gestiona los teclados de confirmación (InlineKeyboard) y la
asociación de reservas por usuario a través de chatbot_memoria.py.
"""

import re
from typing import Any, Dict, List, Optional, Tuple

import chatbot_memoria
from consulta_llm import procesar_mensaje, reiniciar_sesion, obtener_sesion
import almacen_sqlite


def _session_id_telegram(chat_id: int) -> str:
    """Convierte un chat_id de Telegram en un session_id interno."""
    return f"tg_{chat_id}"


def procesar_mensaje_telegram(chat_id: int, texto: str) -> Dict[str, Any]:
    """Procesa un mensaje de texto del usuario y devuelve respuesta + metadatos.

    Returns:
        dict con claves:
            - respuesta (str): Texto de respuesta al usuario.
            - mostrar_confirmacion (bool): Si se debe mostrar teclado de confirmación.
            - reserva_creada (str | None): Código de reserva si se acaba de crear una.
    """
    sid = _session_id_telegram(chat_id)
    respuesta = procesar_mensaje(sid, texto)

    reserva_creada = None
    # Detectar si se creó una reserva exitosamente
    match_codigo = re.search(r"(NOVA-\d{4,})", respuesta)
    if match_codigo and "creada" in respuesta.lower():
        reserva_creada = match_codigo.group(1)
        chatbot_memoria.registrar_reserva_usuario(sid, reserva_creada)

    # Detectar si se está pidiendo confirmación
    mostrar_confirmacion = "confirmas" in respuesta.lower() or "confirmo" in respuesta.lower()

    return {
        "respuesta": respuesta,
        "mostrar_confirmacion": mostrar_confirmacion,
        "reserva_creada": reserva_creada,
    }


def comando_start(chat_id: int) -> str:
    """Maneja el comando /start: da la bienvenida y reinicia la sesión."""
    sid = _session_id_telegram(chat_id)
    reiniciar_sesion(sid)
    return (
        "🏛️ *¡Bienvenido a NovaEventos!*\n\n"
        "Soy tu asistente de reservas. Puedo ayudarte a:\n"
        "• 🎤 Reservar una *Conferencia Corporativa*\n"
        "• 💍 Reservar una *Recepción de Boda*\n"
        "• 🎂 Reservar una *Celebración de Cumpleaños*\n"
        "• 📚 Reservar un *Taller Ejecutivo*\n\n"
        "Escríbeme qué tipo de evento deseas y te guiaré paso a paso.\n\n"
        "📋 *Comandos disponibles:*\n"
        "/start — Reiniciar conversación\n"
        "/ayuda — Ver ayuda completa\n"
        "/reservas — Ver tus reservas\n"
        "/consultar NOVA\\-XXXX — Consultar una reserva\n"
        "/cancelar NOVA\\-XXXX — Cancelar una reserva propia\n"
        "/reiniciar — Limpiar la sesión actual"
    )


def comando_ayuda(chat_id: int) -> str:
    """Maneja el comando /ayuda."""
    return (
        "📖 *Ayuda de NovaEventos*\n\n"
        "*¿Cómo reservar?*\n"
        "Escríbeme un mensaje como:\n"
        "  _\"Quiero reservar una Conferencia para el 2026\\-12\\-01 a las 10:00 "
        "para 60 personas\"_\n\n"
        "El asistente te pedirá los datos faltantes paso a paso\\.\n\n"
        "*Comandos:*\n"
        "/start — Reiniciar conversación\n"
        "/reservas — Ver reservas creadas desde esta cuenta\n"
        "/todas — Ver todas las reservas activas del sistema\n"
        "/consultar `NOVA\\-XXXX` — Ver detalles de una reserva\n"
        "/cancelar `NOVA\\-XXXX` — Cancelar una reserva propia\n"
        "/reiniciar — Limpiar borrador actual\n\n"
        "⏰ *Horario de atención:* 08:00 a 22:00\n"
        "📍 *Espacios:* Auditorio Nova, Salón Imperial, Salón Social, Sala Innovación"
    )


def comando_reiniciar(chat_id: int) -> str:
    """Maneja el comando /reiniciar."""
    sid = _session_id_telegram(chat_id)
    reiniciar_sesion(sid)
    return (
        "🔄 Sesión reiniciada\\.\n\n"
        "¿Qué servicio deseas reservar?\n"
        "• 🎤 Conferencia\n"
        "• 💍 Boda\n"
        "• 🎂 Cumpleaños\n"
        "• 📚 Taller"
    )


def comando_reservas(chat_id: int) -> str:
    """Muestra las reservas creadas por este usuario."""
    sid = _session_id_telegram(chat_id)
    codigos = chatbot_memoria.obtener_reservas_usuario(sid)

    if not codigos:
        return "📋 No tienes reservas registradas desde esta cuenta\\."

    lineas = ["📋 *Tus reservas:*\n"]
    for codigo in codigos:
        reserva = almacen_sqlite.obtener_reserva_por_codigo_db(codigo)
        if reserva:
            icono = "🟢" if reserva["estado"] == "activa" else "🔴"
            lineas.append(
                f"{icono} `{reserva['codigo']}` \\| "
                f"{_escapar_md(reserva['servicio_nombre'])} \\| "
                f"{reserva['fecha']} {reserva['hora_inicio']}\\-{reserva['hora_fin']} \\| "
                f"Estado: {reserva['estado']}"
            )
        else:
            lineas.append(f"⚠️ `{codigo}` — No encontrada en la base de datos")

    return "\n".join(lineas)


def comando_todas(chat_id: int) -> str:
    """Muestra todas las reservas activas del sistema."""
    reservas = almacen_sqlite.listar_reservas_db(estado="activa")

    if not reservas:
        return "📋 No hay reservas activas en el sistema\\."

    lineas = ["📋 *Reservas activas en el sistema:*\n"]
    for r in reservas:
        lineas.append(
            f"🟢 `{r['codigo']}` \\| "
            f"{_escapar_md(r['servicio_nombre'])} \\| "
            f"{_escapar_md(r['espacio'])} \\| "
            f"{r['fecha']} {r['hora_inicio']}\\-{r['hora_fin']} \\| "
            f"{r['asistentes']} personas"
        )

    return "\n".join(lineas)


def comando_consultar(chat_id: int, codigo: str) -> str:
    """Consulta los detalles de una reserva por código."""
    codigo = codigo.strip().upper()

    if not codigo:
        return "⚠️ Uso: `/consultar NOVA\\-XXXX`"

    reserva = almacen_sqlite.obtener_reserva_por_codigo_db(codigo)
    if not reserva:
        return f"❌ No existe la reserva `{_escapar_md(codigo)}`\\."

    icono = "🟢" if reserva["estado"] == "activa" else "🔴"
    return (
        f"🔍 *Detalle de Reserva `{_escapar_md(reserva['codigo'])}`*\n\n"
        f"{icono} *Estado:* {reserva['estado']}\n"
        f"👤 *Cliente:* {_escapar_md(reserva['cliente_nombre'])}\n"
        f"📞 *Contacto:* {_escapar_md(reserva['cliente_contacto'])}\n"
        f"🎪 *Servicio:* {_escapar_md(reserva['servicio_nombre'])}\n"
        f"🏢 *Espacio:* {_escapar_md(reserva['espacio'])}\n"
        f"📅 *Fecha:* {reserva['fecha']}\n"
        f"🕐 *Horario:* {reserva['hora_inicio']} a {reserva['hora_fin']} "
        f"\\({reserva['duracion_horas']}h\\)\n"
        f"👥 *Asistentes:* {reserva['asistentes']}\n"
        f"📝 *Notas:* {_escapar_md(reserva.get('notas', '') or 'Sin notas')}"
    )


def comando_cancelar(chat_id: int, codigo: str) -> str:
    """Cancela una reserva propia del usuario."""
    sid = _session_id_telegram(chat_id)
    codigo = codigo.strip().upper()

    if not codigo:
        return "⚠️ Uso: `/cancelar NOVA\\-XXXX`"

    reserva = almacen_sqlite.obtener_reserva_por_codigo_db(codigo)
    if not reserva:
        return f"❌ No existe la reserva `{_escapar_md(codigo)}`\\."

    if reserva["estado"] == "cancelada":
        return f"ℹ️ La reserva `{_escapar_md(codigo)}` ya está cancelada\\."

    # Verificar propiedad: solo el creador puede cancelar
    if not chatbot_memoria.es_propietario(sid, codigo):
        return (
            f"🚫 *Acceso denegado:* No puedes cancelar la reserva "
            f"`{_escapar_md(codigo)}` porque no fue creada desde esta cuenta\\.\n\n"
            f"Solo el usuario que creó la reserva puede cancelarla\\."
        )

    try:
        cancelada = almacen_sqlite.cancelar_reserva_db(codigo)
        return (
            f"✅ *Reserva `{_escapar_md(cancelada['codigo'])}` cancelada exitosamente\\.*\n\n"
            f"🏢 Espacio liberado: {_escapar_md(cancelada['espacio'])}\n"
            f"📅 Horario liberado: {cancelada['fecha']} de "
            f"{cancelada['hora_inicio']} a {cancelada['hora_fin']}\n\n"
            f"🎉 El espacio queda disponible para nuevas reservas\\."
        )
    except LookupError as e:
        return f"❌ Error: {_escapar_md(str(e))}"


def _escapar_md(texto: str) -> str:
    """Escapa caracteres especiales de MarkdownV2 de Telegram."""
    if not texto:
        return ""
    caracteres = r"_*[]()~`>#+-=|{}.!"
    resultado = ""
    for c in texto:
        if c in caracteres:
            resultado += f"\\{c}"
        else:
            resultado += c
    return resultado


def formatear_respuesta_telegram(texto: str) -> str:
    """Convierte la respuesta del motor conversacional a formato Telegram.

    El motor usa Markdown simple (**negrita**, etc.). Telegram MarkdownV2
    requiere escapado especial. Esta función hace la conversión.
    """
    if not texto:
        return ""

    # Preservar negritas: **texto** → *texto*
    # Primero extraer las negritas, luego escapar, luego reinyectar
    negritas = re.findall(r"\*\*(.+?)\*\*", texto)
    for i, negrita in enumerate(negritas):
        texto = texto.replace(f"**{negrita}**", f"<<BOLD{i}>>", 1)

    # Escapar caracteres especiales de MarkdownV2
    texto = _escapar_md(texto)

    # Reinyectar negritas
    for i, negrita in enumerate(negritas):
        texto = texto.replace(f"<<BOLD{i}>>", f"*{_escapar_md(negrita)}*")

    return texto
