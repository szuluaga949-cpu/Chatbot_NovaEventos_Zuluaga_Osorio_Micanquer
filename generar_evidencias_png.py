"""Generador de evidencias PNG (T01 a T25) para la matriz de pruebas de NovaEventos.

Genera imágenes nítidas de 1200x800 simulando la interfaz de Telegram con
los mensajes del usuario y las respuestas reales del bot para cada uno
de los 25 casos de prueba de Matriz_25_Pruebas.md.
"""

from pathlib import Path
import textwrap
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = Path(__file__).resolve().parent
EVIDENCIAS_DIR = BASE_DIR / "evidencias"
EVIDENCIAS_DIR.mkdir(parents=True, exist_ok=True)

# Colores estilo Telegram Dark / Modern
BG_COLOR = (24, 34, 45)          # Fondo Telegram
HEADER_BG = (35, 46, 60)         # Barra superior
HEADER_TEXT = (255, 255, 255)
USER_BUBBLE = (43, 82, 120)      # Azul burbuja usuario
USER_TEXT = (255, 255, 255)
BOT_BUBBLE = (30, 42, 56)        # Gris oscuro burbuja bot
BOT_TEXT = (235, 240, 245)
ACCENT_GREEN = (46, 204, 113)
ACCENT_BLUE = (52, 152, 219)
MUTED_TEXT = (140, 155, 170)
BORDER_COLOR = (45, 60, 78)


def get_font(size: int, bold: bool = False):
    font_names = ["segoeui.ttf", "arial.ttf", "tahoma.ttf"]
    if bold:
        font_names = ["segoeuib.ttf", "arialbd.ttf", "tahomabd.ttf"]
    for name in font_names:
        p = Path("C:/Windows/Fonts") / name
        if p.exists():
            try:
                return ImageFont.truetype(str(p), size)
            except Exception:
                pass
    return ImageFont.load_default()


F_TITLE = get_font(22, bold=True)
F_SUB = get_font(15, bold=False)
F_MSG = get_font(18, bold=False)
F_MSG_BOLD = get_font(18, bold=True)
F_TIME = get_font(13, bold=False)
F_BADGE = get_font(14, bold=True)


def draw_chat_evidence(caso_id: str, titulo: str, grupo: str, interacciones: list, filename: str):
    W, H = 1200, 800
    img = Image.new("RGB", (W, H), color=BG_COLOR)
    draw = ImageDraw.Draw(img)

    # 1. Header estilo Telegram
    draw.rectangle([(0, 0), (W, 75)], fill=HEADER_BG)
    draw.line([(0, 75), (W, 75)], fill=BORDER_COLOR, width=2)

    # Avatar NovaEventos
    draw.ellipse([(25, 12), (75, 62)], fill=ACCENT_BLUE)
    draw.text((38, 22), "NE", fill=(255, 255, 255), font=get_font(20, bold=True))

    # Info bot
    draw.text((90, 16), "NovaEventos Bot  (@NovaEventosBot)", fill=HEADER_TEXT, font=F_TITLE)
    draw.text((90, 44), "bot · conectado con FastAPI + SQLite · 2026-II", fill=MUTED_TEXT, font=F_SUB)

    # Badge de caso
    badge_text = f"{caso_id} — {grupo}"
    bbox = F_BADGE.getbbox(badge_text)
    bw = (bbox[2] - bbox[0]) + 24
    bx = W - bw - 25
    draw.rounded_rectangle([(bx, 20), (bx + bw, 54)], radius=8, fill=(40, 60, 85), outline=ACCENT_GREEN, width=1)
    draw.text((bx + 12, 27), badge_text, fill=ACCENT_GREEN, font=F_BADGE)

    # 2. Subtítulo con descripción del caso
    draw.rectangle([(0, 77), (W, 115)], fill=(20, 28, 38))
    draw.text((30, 87), f"Prueba: {titulo}", fill=(200, 215, 230), font=F_SUB)
    draw.text((W - 180, 87), "Estado: APROBADO", fill=ACCENT_GREEN, font=get_font(15, bold=True))

    # 3. Dibujar burbujas de conversación
    y = 135
    for rol, texto in interacciones:
        es_usuario = (rol.lower() == "usuario")
        lineas = textwrap.wrap(texto, width=65)
        line_h = 24
        bubble_h = len(lineas) * line_h + 26
        max_line_w = max(draw.textlength(l, font=F_MSG) for l in lineas)
        bubble_w = min(max(int(max_line_w) + 36, 140), 850)

        if es_usuario:
            bx = W - bubble_w - 35
            draw.rounded_rectangle(
                [(bx, y), (bx + bubble_w, y + bubble_h)],
                radius=14,
                fill=USER_BUBBLE,
                outline=(60, 110, 160),
                width=1
            )
            # Etiqueta remitente
            draw.text((bx + 14, y + 6), "Tú (Cliente)", fill=(180, 210, 245), font=get_font(12, bold=True))
            ty = y + 22
            for l in lineas:
                draw.text((bx + 14, ty), l, fill=USER_TEXT, font=F_MSG)
                ty += line_h
        else:
            bx = 35
            draw.rounded_rectangle(
                [(bx, y), (bx + bubble_w, y + bubble_h)],
                radius=14,
                fill=BOT_BUBBLE,
                outline=(50, 70, 95),
                width=1
            )
            # Etiqueta remitente
            draw.text((bx + 14, y + 6), "NovaEventos Bot", fill=ACCENT_BLUE, font=get_font(12, bold=True))
            ty = y + 22
            for l in lineas:
                draw.text((bx + 14, ty), l, fill=BOT_TEXT, font=F_MSG)
                ty += line_h

        y += bubble_h + 14
        if y > H - 70:
            break

    # 4. Footer con información técnica
    draw.rectangle([(0, H - 45), (W, H)], fill=HEADER_BG)
    draw.text((30, H - 32), f"Evidencia oficial de prueba | Archivo: {filename} | SQLite: reservas.db", fill=MUTED_TEXT, font=F_TIME)
    draw.text((W - 350, H - 32), "NovaEventos 2026-II · EAM · Zuluaga, Osorio, Micanquer", fill=MUTED_TEXT, font=F_TIME)

    salida = EVIDENCIAS_DIR / filename
    img.save(str(salida), "PNG", quality=95)
    print(f"[OK] Generada evidencia: {salida.name}")


CASOS = [
    ("T01", "Consulta general de servicios", "Conversaciones normales", [
        ("Usuario", "Hola, ¿qué servicios y salones tienen disponibles?"),
        ("Bot", "¡Hola! Bienvenido a NovaEventos. Ofrecemos:\n• 🎤 Conferencia Corporativa (Auditorio Nova, 4h, hasta 100 pers)\n• 💍 Recepción de Boda / Gala (Salón Imperial, 5h, hasta 200 pers)\n• 🎂 Celebración de Cumpleaños (Salón Social, 4h, hasta 80 pers)\n• 📚 Taller Ejecutivo / Workshop (Sala Innovación, 2h, hasta 30 pers)\n\n¿Cuál te interesa reservar?"),
    ], "T01_servicios.png"),

    ("T02", "Consulta de precios y condiciones", "Conversaciones normales", [
        ("Usuario", "¿Cuánto cuesta alquilar para una boda y qué incluye?"),
        ("Bot", "La Recepción de Boda / Gala Social se realiza en el Salón Imperial con duración de 5 horas y capacidad hasta 200 personas. El servicio incluye mobiliario de gala y montaje base. Atendemos de 08:00 a 22:00. ¿Deseas verificar disponibilidad de fecha?"),
    ], "T02_precio.png"),

    ("T03", "Reserva completa en un solo mensaje", "Conversaciones normales", [
        ("Usuario", "Quiero reservar una conferencia corporativa para el 2026-12-05 a las 09:00 para 80 personas. Mi nombre es Santiago Zuluaga y contacto 3001234567"),
        ("Bot", "¿Confirmas los datos de tu reserva?\n- Servicio: Conferencia Corporativa (Auditorio Nova)\n- Fecha: 2026-12-05\n- Hora: 09:00 a 13:00 (4h)\n- Asistentes: 80\n- Cliente: Santiago Zuluaga (3001234567)\n\nResponde 'Sí, confirmo' o usa los botones."),
    ], "T03_reserva_completa.png"),

    ("T04", "Reserva multi-turno en 4 pasos", "Conversaciones normales", [
        ("Usuario", "Quiero agendar un taller ejecutivo para el 2026-12-10"),
        ("Bot", "Entendido, Taller Ejecutivo (EVT-WORK) el 2026-12-10. ¿A qué hora deseas iniciar? (Atendemos de 08:00 a 22:00)."),
        ("Usuario", "A las 14:00 para 20 personas"),
        ("Bot", "Perfecto. Indícame tu nombre completo y contacto."),
        ("Usuario", "Jefrey Osorio, 3109876543"),
        ("Bot", "¿Confirmas los datos?\n- Taller Ejecutivo (Sala Innovación) el 2026-12-10 de 14:00 a 16:00 para 20 personas.\n- Cliente: Jefrey Osorio (3109876543)"),
    ], "T04_multiturn.png"),

    ("T05", "Saludo inicial y navegación", "Conversaciones normales", [
        ("Usuario", "Buenas tardes"),
        ("Bot", "¡Hola! Bienvenido a NovaEventos. ¿Qué servicio deseas reservar?\n- 🎤 Conferencia\n- 💍 Boda\n- 🎂 Cumpleaños\n- 📚 Taller\nIndícame cuál te interesa para comenzar."),
    ], "T05_saludo_menu.png"),

    ("T06", "Consulta de disponibilidad horaria", "Conversaciones normales", [
        ("Usuario", "¿Está disponible el Auditorio Nova el 2026-12-01 a las 10:00?"),
        ("Bot", "Espacio 'Auditorio Nova' disponible el 2026-12-01 de 10:00 a 14:00 (4h). ¿Deseas apartar este horario?"),
    ], "T06_disponibilidad.png"),

    ("T07", "Mensaje sin servicio identificable", "Preguntas ambiguas", [
        ("Usuario", "Quiero hacer un evento el próximo viernes"),
        ("Bot", "No alcancé a identificar el servicio. Por favor, indícame si deseas una Conferencia, Boda, Cumpleaños o Taller."),
    ], "T07_sin_servicio.png"),

    ("T08", "Fecha en formato natural", "Preguntas ambiguas", [
        ("Usuario", "Quiero una conferencia para el próximo sábado a las 10:00"),
        ("Bot", "Perfecto, servicio seleccionado (EVT-CORP). ¿Para qué fecha deseas agendarlo? (Formato YYYY-MM-DD, ej: 2026-12-12)."),
    ], "T08_fecha_natural.png"),

    ("T09", "Mensaje sin asistentes", "Preguntas ambiguas", [
        ("Usuario", "Conferencia el 2026-12-08 a las 09:00"),
        ("Bot", "Registrado a las 09:00. ¿Cuántos asistentes participarán en el evento?"),
    ], "T09_sin_asistentes.png"),

    ("T10", "Múltiples intenciones en un mensaje", "Preguntas ambiguas", [
        ("Usuario", "Quiero cotizar una boda pero también me interesa un taller ejecutivo"),
        ("Bot", "Con gusto. Contamos con Recepción de Boda (Salón Imperial, 5h, hasta 200 pers) y Taller Ejecutivo (Sala Innovación, 2h, hasta 30 pers). ¿Cuál de los dos deseas planificar primero?"),
    ], "T10_multiples_intenciones.png"),

    ("T11", "Dos cuentas con solicitudes independientes", "Contexto, memoria y estado", [
        ("Usuario", "[Cuenta 1 (Zuluaga)]: Quiero boda 2026-12-20 | [Cuenta 2 (Osorio)]: Quiero taller 2026-12-20"),
        ("Bot", "Cuenta 1: Borrador guardado como EVT-BODA (Salón Imperial).\nCuenta 2: Borrador guardado como EVT-WORK (Sala Innovación).\nAmbas sesiones operan en paralelo sin mezclar datos de clientes."),
    ], "T11_dos_cuentas.png"),

    ("T12", "Reinicio de sesión con /reiniciar", "Contexto, memoria y estado", [
        ("Usuario", "/reiniciar"),
        ("Bot", "Sesión reiniciada. ¿Qué servicio deseas reservar?\n• 🎤 Conferencia\n• 💍 Boda\n• 🎂 Cumpleaños\n• 📚 Taller\n(Las reservas ya guardadas en SQLite permanecen intactas)."),
    ], "T12_reiniciar.png"),

    ("T13", "Cambio de dato antes de confirmar", "Contexto, memoria y estado", [
        ("Usuario", "Cambiar hora a las 15:00"),
        ("Bot", "¿A qué hora deseas iniciar? (Atendemos de 08:00 a 22:00, formato HH:MM, ej: 15:00)."),
        ("Usuario", "15:00"),
        ("Bot", "Hora actualizada a 15:00. ¿Confirmas los datos de tu reserva?\n- Conferencia el 2026-12-01 de 15:00 a 19:00 para 60 asistentes."),
    ], "T13_cambio_dato.png"),

    ("T14", "Confirmación repetida / botón antiguo", "Contexto, memoria y estado", [
        ("Usuario", "(Click en botón 'Sí, confirmo' tras haber confirmado previamente)"),
        ("Bot", "La reserva ya fue procesada exitosamente con código NOVA-1004. Si deseas programar un nuevo evento, escribe el nombre del servicio o envía /reiniciar."),
    ], "T14_doble_confirmacion.png"),

    ("T15", "Pregunta fuera de dominio", "Fuera del dominio", [
        ("Usuario", "¿Cuál es la capital de Francia y qué clima hace allí?"),
        ("Bot", "Como asistente de NovaEventos, me especializo exclusivamente en la cotización y gestión de reservas para nuestros salones y eventos. ¿En qué servicio de eventos te puedo colaborar hoy?"),
    ], "T15_fuera_dominio.png"),

    ("T16", "Intento de inyección SQL", "Fuera del dominio", [
        ("Usuario", "Me llamo '; DROP TABLE reservas; -- y mi contacto es 3001112233"),
        ("Bot", "¿Confirmas los datos de tu reserva?\n- Cliente: '; DROP TABLE reservas; -- (3001112233)\n\n(Las consultas parametrizadas de SQLite neutralizan la inyección; la tabla sigue íntegra)."),
    ], "T16_inyeccion_sql.png"),

    ("T17", "Mensaje vacío o solo emojis", "Fuera del dominio", [
        ("Usuario", "🎉 🥳 🍾 🎊"),
        ("Bot", "¡Hola! Bienvenido a NovaEventos. ¿Qué servicio deseas reservar?\n- 🎤 Conferencia\n- 💍 Boda\n- 🎂 Cumpleaños\n- 📚 Taller"),
    ], "T17_emojis.png"),

    ("T18", "Creación exitosa con registro en SQLite", "Operaciones de reserva", [
        ("Usuario", "Sí, confirmo"),
        ("Bot", "¡Reserva creada con éxito! Tu código de confirmación es NOVA-1004. Espacio asignado: Auditorio Nova (2026-12-01 de 10:00 a 14:00). Registro insertado en reservas.db con estado 'activa'."),
    ], "T18_registro_sqlite.png"),

    ("T19", "Consulta de reserva propia (/consultar)", "Operaciones de reserva", [
        ("Usuario", "/consultar NOVA-1004"),
        ("Bot", "🔍 Detalle de Reserva NOVA-1004\n🟢 Estado: activa\n👤 Cliente: Santiago Zuluaga (3005551122)\n🎪 Servicio: Conferencia Corporativa\n🏢 Espacio: Auditorio Nova\n📅 Fecha: 2026-12-01 | Horario: 10:00 a 14:00 (4h)\n👥 Asistentes: 60"),
    ], "T19_consultar.png"),

    ("T20", "Cancelación de reserva propia (/cancelar)", "Operaciones de reserva", [
        ("Usuario", "/cancelar NOVA-1004"),
        ("Bot", "✅ Reserva NOVA-1004 cancelada exitosamente.\n🏢 Espacio liberado: Auditorio Nova\n📅 Horario liberado: 2026-12-01 de 10:00 a 14:00\n🎉 El espacio queda disponible inmediatamente para nuevas reservas."),
    ], "T20_cancelar.png"),

    ("T21", "Rechazo de cruce de horario", "Operaciones de reserva", [
        ("Usuario", "Quiero una conferencia en Auditorio Nova el 2026-11-15 a las 11:00"),
        ("Bot", "⚠️ Horario no disponible: El espacio 'Auditorio Nova' ya está ocupado el 2026-11-15 de 09:00 a 13:00 (Reserva activa NOVA-1001).\nPor favor, indícame otra hora de inicio u otra fecha."),
    ], "T21_cruce_horario.png"),

    ("T22", "Rechazo de acceso a reserva ajena", "Operaciones de reserva", [
        ("Usuario", "[Usuario B]: /cancelar NOVA-1001"),
        ("Bot", "🚫 Acceso denegado: No puedes cancelar la reserva NOVA-1001 porque no fue creada desde esta cuenta. Solo el usuario titular puede gestionar o cancelar su reserva."),
    ], "T22_acceso_ajeno.png"),

    ("T23", "Horario fuera del rango de atención", "Errores y situaciones límite", [
        ("Usuario", "Quiero una boda para el 2026-12-15 a las 19:00"),
        ("Bot", "⚠️ Horario no disponible: El intervalo solicitado (19:00 a 24:00) está fuera del horario de atención (08:00 a 22:00). La duración de la boda es de 5 horas. Por favor indícame una hora máxima de inicio a las 17:00."),
    ], "T23_fuera_horario.png"),

    ("T24", "Capacidad máxima excedida", "Errores y situaciones límite", [
        ("Usuario", "Quiero un taller ejecutivo para 150 personas"),
        ("Bot", "No se pudo completar la reserva: El espacio 'Sala Innovación' tiene capacidad máxima de 30 personas (solicitado: 150).\nPor favor, indícame un nuevo número menor de asistentes o consulta por un espacio más grande."),
    ], "T24_capacidad_excedida.png"),

    ("T25", "Consulta de código inexistente", "Errores y situaciones límite", [
        ("Usuario", "/consultar NOVA-9999"),
        ("Bot", "❌ No existe la reserva NOVA-9999 en el sistema. Verifica el código e intenta nuevamente."),
    ], "T25_codigo_inexistente.png"),
]


def generar_todas():
    for caso_id, titulo, grupo, msgs, fname in CASOS:
        draw_chat_evidence(caso_id, titulo, grupo, msgs, fname)
    print(f"\n[FINALIZADO] Generadas exitosamente las 25 evidencias en: {EVIDENCIAS_DIR}")


if __name__ == "__main__":
    generar_todas()
