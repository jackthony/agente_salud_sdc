"""Tools del agente — simuladas para la clase.

En producción, estas tools llamarían APIs reales (MINSA, HIS hospitalario, Google Places).
Para la clase usamos datos sintéticos pero realistas.
"""
from __future__ import annotations

from datetime import datetime

from agents import function_tool

from .schemas import Hospital, Protocolo

PROTOCOLOS_DB: dict[str, Protocolo] = {
    "dolor_toracico": Protocolo(
        titulo="Protocolo Dolor Torácico Agudo",
        pasos=[
            "Evaluar ABCDE (vía aérea, respiración, circulación)",
            "ECG de 12 derivaciones en <10 min",
            "Troponina si sospecha IAM",
            "Traslado a UCI coronaria si confirmado",
        ],
        fuente="MINSA Perú - Guía Cardiología 2023",
    ),
    "acv": Protocolo(
        titulo="Protocolo Sospecha ACV",
        pasos=[
            "Aplicar escala FAST (Face-Arms-Speech-Time)",
            "TAC cerebral sin contraste <25 min",
            "Ventana trombólisis: 4.5 horas desde inicio",
            "Activar código ictus",
        ],
        fuente="MINSA Perú - Guía Neurología 2023",
    ),
    "fiebre_pediatrica": Protocolo(
        titulo="Protocolo Fiebre en Pediatría",
        pasos=[
            "Medir temperatura rectal/axilar",
            "Evaluar signos de sepsis",
            "Antipirético según peso",
            "Hidratación oral",
        ],
        fuente="MINSA Perú - Guía Pediatría 2023",
    ),
    "resfriado_comun": Protocolo(
        titulo="Resfriado Común - Autocuidado",
        pasos=[
            "Reposo y abundantes líquidos",
            "Paracetamol si malestar",
            "Consultar si >7 días o fiebre >38.5°C persistente",
        ],
        fuente="OMS - Guía Infecciones Respiratorias",
    ),
}

HOSPITALES_DB: list[Hospital] = [
    Hospital(nombre="Hospital Nacional Dos de Mayo", distrito="Cercado de Lima", espera_min=45, capacidad="media"),
    Hospital(nombre="Hospital Edgardo Rebagliati", distrito="Jesús María", espera_min=90, capacidad="alta"),
    Hospital(nombre="Hospital Loayza", distrito="Cercado de Lima", espera_min=60, capacidad="media"),
    Hospital(nombre="Clínica Ricardo Palma", distrito="San Isidro", espera_min=20, capacidad="baja"),
    Hospital(nombre="Clínica Internacional", distrito="San Borja", espera_min=25, capacidad="baja"),
    Hospital(nombre="Hospital Cayetano Heredia", distrito="San Martín de Porres", espera_min=70, capacidad="alta"),
]


@function_tool
def consultar_protocolo_minsa(condicion: str) -> str:
    """Busca protocolo clínico oficial MINSA Perú para una condición.

    Args:
        condicion: Nombre corto de la condición. Opciones válidas:
            dolor_toracico, acv, fiebre_pediatrica, resfriado_comun.
    """
    key = condicion.strip().lower().replace(" ", "_")
    if key not in PROTOCOLOS_DB:
        return f"Protocolo '{condicion}' no encontrado. Disponibles: {', '.join(PROTOCOLOS_DB)}"
    p = PROTOCOLOS_DB[key]
    pasos = "\n".join(f"  {i+1}. {s}" for i, s in enumerate(p.pasos))
    return f"{p.titulo}\n{pasos}\nFuente: {p.fuente}"


@function_tool
def buscar_hospital_cercano(distrito: str, urgencia: str) -> str:
    """Busca hospital/clínica más cercana según distrito y urgencia.

    Args:
        distrito: Distrito del paciente (ej: San Isidro, Lima).
        urgencia: ROJO (emergencia), AMARILLO (urgente), VERDE (no urgente).
    """
    candidatos = [h for h in HOSPITALES_DB if distrito.lower() in h.distrito.lower()]
    if not candidatos:
        candidatos = HOSPITALES_DB

    if urgencia.upper() == "ROJO":
        candidatos = [h for h in candidatos if h.capacidad in ("alta", "media")]

    candidatos = sorted(candidatos, key=lambda h: h.espera_min)
    if not candidatos:
        return "No se encontró hospital disponible. Llame al 106 (SAMU)."
    mejor = candidatos[0]
    return (
        f"Sugerido: {mejor.nombre} ({mejor.distrito}) - "
        f"espera ~{mejor.espera_min} min - capacidad: {mejor.capacidad}"
    )


@function_tool
def registrar_caso_auditoria(nivel: str, razon: str) -> str:
    """Registra el caso en el log de auditoría (requerido por compliance).

    Args:
        nivel: Nivel de triage (ROJO, AMARILLO, VERDE).
        razon: Razón del triage para el registro.
    """
    ts = datetime.now().isoformat(timespec="seconds")
    entry = f"[{ts}] nivel={nivel} razon={razon[:100]}"
    # En prod: escribir a DB / SIEM
    return f"Registrado: {entry}"


TRIAGE_TOOLS = [
    consultar_protocolo_minsa,
    buscar_hospital_cercano,
    registrar_caso_auditoria,
]
