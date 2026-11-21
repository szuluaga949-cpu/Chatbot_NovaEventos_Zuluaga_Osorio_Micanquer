"""Bot de Telegram para NovaEventos.

Escucha mensajes y comandos de los usuarios en Telegram, los enruta
al motor conversacional a través de api_telegram.py y devuelve las
respuestas formateadas. Soporta múltiples usuarios simultáneamente,
cada chat_id opera como una sesión independiente.

Ejecución:
    .venv/Scripts/python bot_telegram.py

Variables de entorno requeridas:
    TELEGRAM_BOT_TOKEN — Token del bot proporcionado por @BotFather
    CHATBOT_API_URL    — URL donde corre FastAPI (por defecto http://127.0.0.1:8011)
"""

import logging
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    MessageHandler,
    filters,
)

# Cargar variables de entorno desde .env
load_dotenv(Path(__file__).resolve().parent / ".env")

import api_telegram
from api_telegram import (
    comando_ayuda,
    comando_cancelar,
    comando_consultar,
    comando_reiniciar,
    comando_reservas,
    comando_start,
    comando_todas,
    formatear_respuesta_telegram,
    procesar_mensaje_telegram,
)

# ── Configuración ─────────────────────────────────────────────────────
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")

logging.basicConfig(
    format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger("NovaEventos-Bot")


# ── Handlers de comandos ──────────────────────────────────────────────

async def handler_start(update: Update, context) -> None:
    """Comando /start — Bienvenida y reinicio de sesión."""
    respuesta = comando_start(update.effective_chat.id)
    await update.message.reply_text(respuesta, parse_mode="MarkdownV2")


async def handler_ayuda(update: Update, context) -> None:
    """Comando /ayuda — Muestra la ayuda completa."""
    respuesta = comando_ayuda(update.effective_chat.id)
    await update.message.reply_text(respuesta, parse_mode="MarkdownV2")


async def handler_reiniciar(update: Update, context) -> None:
    """Comando /reiniciar — Limpia la sesión actual."""
    respuesta = comando_reiniciar(update.effective_chat.id)
    await update.message.reply_text(respuesta, parse_mode="MarkdownV2")


async def handler_reservas(update: Update, context) -> None:
    """Comando /reservas — Lista las reservas del usuario."""
    respuesta = comando_reservas(update.effective_chat.id)
    await update.message.reply_text(respuesta, parse_mode="MarkdownV2")


async def handler_todas(update: Update, context) -> None:
    """Comando /todas — Lista todas las reservas activas del sistema."""
    respuesta = comando_todas(update.effective_chat.id)
    await update.message.reply_text(respuesta, parse_mode="MarkdownV2")


async def handler_consultar(update: Update, context) -> None:
    """Comando /consultar NOVA-XXXX — Consulta detalles de una reserva."""
    codigo = " ".join(context.args) if context.args else ""
    respuesta = comando_consultar(update.effective_chat.id, codigo)
    await update.message.reply_text(respuesta, parse_mode="MarkdownV2")


async def handler_cancelar(update: Update, context) -> None:
    """Comando /cancelar NOVA-XXXX — Cancela una reserva propia."""
    codigo = " ".join(context.args) if context.args else ""
    respuesta = comando_cancelar(update.effective_chat.id, codigo)
    await update.message.reply_text(respuesta, parse_mode="MarkdownV2")


# ── Handler de mensajes de texto ──────────────────────────────────────

async def handler_mensaje(update: Update, context) -> None:
    """Procesa mensajes de texto a través del motor conversacional."""
    chat_id = update.effective_chat.id
    texto = update.message.text.strip()

    if not texto:
        return

    resultado = procesar_mensaje_telegram(chat_id, texto)
    respuesta_formateada = formatear_respuesta_telegram(resultado["respuesta"])

    # Si requiere confirmación, mostrar teclado inline
    if resultado["mostrar_confirmacion"]:
        teclado = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("✅ Sí, confirmo", callback_data="confirmar"),
                InlineKeyboardButton("❌ Cancelar", callback_data="cancelar_borrador"),
            ]
        ])
        await update.message.reply_text(
            respuesta_formateada,
            parse_mode="MarkdownV2",
            reply_markup=teclado,
        )
    else:
        await update.message.reply_text(
            respuesta_formateada,
            parse_mode="MarkdownV2",
        )


# ── Handler de botones inline (confirmación) ──────────────────────────

async def handler_callback(update: Update, context) -> None:
    """Procesa los botones de confirmación/cancelación inline."""
    query = update.callback_query
    await query.answer()

    chat_id = query.message.chat_id
    accion = query.data

    if accion == "confirmar":
        resultado = procesar_mensaje_telegram(chat_id, "Sí, confirmo")
    elif accion == "cancelar_borrador":
        resultado = procesar_mensaje_telegram(chat_id, "cancelar")
    else:
        return

    respuesta_formateada = formatear_respuesta_telegram(resultado["respuesta"])

    await query.edit_message_text(
        text=respuesta_formateada,
        parse_mode="MarkdownV2",
    )


# ── Punto de entrada ──────────────────────────────────────────────────

def main() -> None:
    """Inicia el bot de Telegram en modo polling."""
    if not TELEGRAM_BOT_TOKEN:
        logger.error(
            "No se encontró TELEGRAM_BOT_TOKEN. "
            "Configúralo en el archivo .env o como variable de entorno."
        )
        sys.exit(1)

    logger.info("Iniciando bot de Telegram NovaEventos...")
    logger.info("Presiona Ctrl+C para detener el bot.")

    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Registrar handlers de comandos
    app.add_handler(CommandHandler("start", handler_start))
    app.add_handler(CommandHandler("ayuda", handler_ayuda))
    app.add_handler(CommandHandler("help", handler_ayuda))
    app.add_handler(CommandHandler("reiniciar", handler_reiniciar))
    app.add_handler(CommandHandler("reservas", handler_reservas))
    app.add_handler(CommandHandler("todas", handler_todas))
    app.add_handler(CommandHandler("consultar", handler_consultar))
    app.add_handler(CommandHandler("cancelar", handler_cancelar))

    # Handler de mensajes de texto (cualquier mensaje que no sea comando)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handler_mensaje))

    # Handler de callbacks de botones inline
    app.add_handler(CallbackQueryHandler(handler_callback))

    # Iniciar polling
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
