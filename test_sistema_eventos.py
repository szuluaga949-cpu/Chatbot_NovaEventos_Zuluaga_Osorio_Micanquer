import os
import tempfile
from pathlib import Path
from fastapi.testclient import TestClient

import almacen_sqlite
import main
import consulta_llm
import chatbot_memoria
import api_telegram


def configurar_entorno_pruebas():
    temp_dir = tempfile.mkdtemp()
    test_db = Path(temp_dir) / "test_reservas.db"
    almacen_sqlite.DB_PATH = test_db
    almacen_sqlite.inicializar_bd(test_db, poblar_semilla=True)
    client = TestClient(main.app)

    def mock_llamar_api(metodo, ruta, params=None, json_body=None):
        resp = client.request(metodo, ruta, params=params, json=json_body)
        datos = resp.json() if resp.content else {}
        if resp.status_code >= 400:
            return {"ok": False, "status": resp.status_code, "error": datos.get("detail", "Error")}
        return {"ok": True, "status": resp.status_code, "data": datos}

    consulta_llm._llamar_api = mock_llamar_api
    consulta_llm.GROQ_API_KEY = ""
    return client, test_db


def test_1_conversacion_varios_turnos_y_creacion():
    _, _ = configurar_entorno_pruebas()
    sid = "test_multi_turno"
    consulta_llm.reiniciar_sesion(sid)

    r1 = consulta_llm.procesar_mensaje(sid, "Quiero reservar una Conferencia Corporativa para el 2026-12-01")
    assert "hora" in r1.lower()

    r2 = consulta_llm.procesar_mensaje(sid, "A las 10:00 para 60 asistentes")
    assert "nombre" in r2.lower()

    r3 = consulta_llm.procesar_mensaje(sid, "Me llamo Santiago Zuluaga y mi contacto es 3005551122")
    assert "confirmas" in r3.lower()

    r4 = consulta_llm.procesar_mensaje(sid, "Sí, confirmo")
    assert "NOVA-1004" in r4


def test_2_dos_sesiones_y_reinicio():
    _, _ = configurar_entorno_pruebas()
    consulta_llm.reiniciar_sesion("S1")
    consulta_llm.reiniciar_sesion("S2")

    consulta_llm.procesar_mensaje("S1", "Quiero reservar una boda para el 2026-12-10")
    consulta_llm.procesar_mensaje("S2", "Quiero un taller para el 2026-12-12")

    assert consulta_llm.obtener_sesion("S1")["borrador"]["servicio_id"] == "EVT-BODA"
    assert consulta_llm.obtener_sesion("S2")["borrador"]["servicio_id"] == "EVT-WORK"

    consulta_llm.reiniciar_sesion("S1")
    assert consulta_llm.obtener_sesion("S1")["borrador"]["servicio_id"] is None
    assert consulta_llm.obtener_sesion("S2")["borrador"]["servicio_id"] == "EVT-WORK"


def test_3_rechazo_intervalos_ocupados_y_cancelacion():
    client, _ = configurar_entorno_pruebas()

    cruce = client.post(
        "/reservas",
        json={
            "cliente_nombre": "Pedro Pérez",
            "cliente_contacto": "3100001122",
            "servicio_id": "EVT-CORP",
            "fecha": "2026-11-15",
            "hora_inicio": "11:00",
            "asistentes": 50,
        },
    )
    assert cruce.status_code == 409
    assert "NOVA-1001" in cruce.json()["detail"]

    canc = client.delete("/reservas/NOVA-1001")
    assert canc.status_code == 200
    assert canc.json()["reserva"]["estado"] == "cancelada"

    exito = client.post(
        "/reservas",
        json={
            "cliente_nombre": "Pedro Pérez",
            "cliente_contacto": "3100001122",
            "servicio_id": "EVT-CORP",
            "fecha": "2026-11-15",
            "hora_inicio": "11:00",
            "asistentes": 50,
        },
    )
    assert exito.status_code == 201


def test_4_memoria_propiedad_reservas():
    """Valida la asignación y verificación de propiedad de reservas por usuario."""
    chatbot_memoria.registrar_reserva_usuario("user_A", "NOVA-1004")
    assert chatbot_memoria.es_propietario("user_A", "NOVA-1004") is True
    assert chatbot_memoria.es_propietario("user_B", "NOVA-1004") is False
    assert "NOVA-1004" in chatbot_memoria.obtener_reservas_usuario("user_A")


def test_5_api_telegram_comandos_basicos():
    """Valida comandos informativos de Telegram."""
    _, _ = configurar_entorno_pruebas()
    resp_start = api_telegram.comando_start(12345)
    assert "Bienvenido" in resp_start

    resp_ayuda = api_telegram.comando_ayuda(12345)
    assert "Ayuda" in resp_ayuda

    resp_todas = api_telegram.comando_todas(12345)
    assert "NOVA-1001" in resp_todas


def test_6_api_telegram_control_acceso_cancelacion():
    """Valida que un usuario no pueda cancelar la reserva de otro usuario."""
    _, _ = configurar_entorno_pruebas()
    # Usuario A (chat_id: 111) crea NOVA-1001 (simulado)
    chatbot_memoria.registrar_reserva_usuario("tg_111", "NOVA-1001")

    # Usuario B (chat_id: 222) intenta cancelar NOVA-1001
    resp_cancel = api_telegram.comando_cancelar(222, "NOVA-1001")
    assert "denegado" in resp_cancel.lower()
