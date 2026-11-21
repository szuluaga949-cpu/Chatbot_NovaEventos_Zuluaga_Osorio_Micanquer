"""Módulo de gestión de memoria y sesiones para NovaEventos.

Centraliza el almacenamiento en memoria del estado de cada conversación
(historial, borrador de reserva) e implementa la asociación de reservas
por usuario (chat_id de Telegram o session_id de Gradio) para verificar
propiedad durante modificaciones y cancelaciones.
"""

from typing import Any, Dict, List, Optional, Set

# ── Estado global en memoria ──────────────────────────────────────────
_sesiones: Dict[str, Dict[str, Any]] = {}
_reservas_por_usuario: Dict[str, Set[str]] = {}  # session_id → {NOVA-XXXX, …}


# ── Sesiones ──────────────────────────────────────────────────────────
def obtener_sesion(session_id: str) -> Dict[str, Any]:
    """Devuelve la sesión existente o crea una nueva con borrador vacío."""
    if session_id not in _sesiones:
        sesion: Dict[str, Any] = {
            "servicio_id": None,
            "fecha": None,
            "hora_inicio": None,
            "asistentes": None,
            "cliente_nombre": None,
            "cliente_contacto": None,
            "notas": "",
        }
        sesion["borrador"] = sesion  # Compatibilidad con tests existentes
        _sesiones[session_id] = sesion
    return _sesiones[session_id]


def reiniciar_sesion(session_id: str) -> None:
    """Elimina el borrador y el historial de la sesión indicada."""
    if session_id in _sesiones:
        del _sesiones[session_id]
    obtener_sesion(session_id)


def listar_sesiones_activas() -> List[str]:
    """Devuelve la lista de session_ids con sesiones activas."""
    return list(_sesiones.keys())


def obtener_borrador(session_id: str) -> Dict[str, Any]:
    """Devuelve solo los campos del borrador de reserva de la sesión."""
    sesion = obtener_sesion(session_id)
    campos = [
        "servicio_id", "fecha", "hora_inicio",
        "asistentes", "cliente_nombre", "cliente_contacto", "notas",
    ]
    return {k: sesion.get(k) for k in campos}


def sesion_tiene_datos(session_id: str) -> bool:
    """Verifica si la sesión tiene al menos un campo del borrador lleno."""
    borrador = obtener_borrador(session_id)
    return any(v not in (None, "") for k, v in borrador.items() if k != "notas")


# ── Propiedad de reservas por usuario ─────────────────────────────────
def registrar_reserva_usuario(session_id: str, codigo_reserva: str) -> None:
    """Asocia un código de reserva al usuario que la creó."""
    if session_id not in _reservas_por_usuario:
        _reservas_por_usuario[session_id] = set()
    _reservas_por_usuario[session_id].add(codigo_reserva.upper())


def es_propietario(session_id: str, codigo_reserva: str) -> bool:
    """Verifica si el usuario (session_id) creó la reserva indicada."""
    codigos = _reservas_por_usuario.get(session_id, set())
    return codigo_reserva.upper() in codigos


def obtener_reservas_usuario(session_id: str) -> List[str]:
    """Devuelve la lista de códigos de reserva creados por el usuario."""
    return sorted(_reservas_por_usuario.get(session_id, set()))


def total_sesiones() -> int:
    """Devuelve el número total de sesiones activas en memoria."""
    return len(_sesiones)
