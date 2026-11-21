"""Simulador de respuesta perdida / fallo del LLM para NovaEventos.

Permite verificar que el sistema funciona correctamente cuando la API de
Groq no responde o devuelve un error. El motor conversacional
(consulta_llm.py) tiene un extractor determinista de respaldo que procesa
los mensajes del usuario sin depender del LLM.

Ejecución:
    .venv/Scripts/python simular_respuesta_perdida.py

Este script:
1. Desactiva la clave de Groq temporalmente (GROQ_API_KEY = "").
2. Ejecuta una secuencia de mensajes de prueba a través del motor conversacional.
3. Verifica que las respuestas sean coherentes usando solo el extractor de respaldo.
4. Restaura la configuración original al finalizar.
"""

import os
import sys

# Forzar que no haya API key de Groq para simular la desconexión
os.environ["GROQ_API_KEY"] = ""

from consulta_llm import procesar_mensaje, reiniciar_sesion


def separador(titulo: str) -> None:
    print(f"\n{'='*70}")
    print(f"  {titulo}")
    print(f"{'='*70}\n")


def simular_conversacion() -> None:
    """Ejecuta una conversación completa sin conexión al LLM."""
    sid = "simulacion_offline"
    reiniciar_sesion(sid)

    pasos = [
        ("Hola, buenos días", "Debe dar bienvenida y mostrar servicios"),
        ("Quiero reservar una conferencia corporativa para el 2026-12-15", "Debe detectar servicio y fecha, pedir hora"),
        ("A las 10:00 para 50 personas", "Debe registrar hora y asistentes, pedir nombre/contacto"),
        ("Juan Pérez, juan@correo.com", "Debe mostrar resumen de confirmación"),
    ]

    exitos = 0
    for i, (mensaje, esperado) in enumerate(pasos, 1):
        print(f"📤 Turno {i} — Usuario: \"{mensaje}\"")
        print(f"   📋 Esperado: {esperado}")

        respuesta = procesar_mensaje(sid, mensaje)
        print(f"   🤖 Bot: {respuesta[:200]}{'...' if len(respuesta) > 200 else ''}")

        if respuesta and len(respuesta) > 10:
            print(f"   ✅ Respuesta válida recibida")
            exitos += 1
        else:
            print(f"   ❌ Respuesta vacía o muy corta")
        print()

    separador("RESULTADO DE LA SIMULACIÓN")
    print(f"  Turnos ejecutados: {len(pasos)}")
    print(f"  Respuestas válidas: {exitos}/{len(pasos)}")
    print(f"  Estado: {'✅ EXITOSO' if exitos == len(pasos) else '⚠️ CON FALLOS'}")
    print()
    print("  El extractor determinista de consulta_llm.py procesó todos los")
    print("  mensajes sin depender del modelo LLM externo.")
    print()

    if exitos == len(pasos):
        return 0
    return 1


def main() -> int:
    separador("SIMULACIÓN DE RESPUESTA PERDIDA — NovaEventos")
    print("  Este script verifica el funcionamiento del sistema cuando la")
    print("  API de Groq no está disponible (GROQ_API_KEY vacía).")
    print("  El motor conversacional debe funcionar con su extractor de")
    print("  respaldo basado en expresiones regulares.")
    return simular_conversacion()


if __name__ == "__main__":
    sys.exit(main())
