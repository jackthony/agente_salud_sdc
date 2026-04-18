"""Schemas Pydantic — Zero-Hallucination por structured output."""
from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field


class NivelTriage(str, Enum):
    ROJO = "ROJO"
    AMARILLO = "AMARILLO"
    VERDE = "VERDE"


class AccionRecomendada(str, Enum):
    LLAMAR_AMBULANCIA = "LLAMAR_AMBULANCIA"
    IR_EMERGENCIA = "IR_EMERGENCIA"
    CONSULTA_HOY = "CONSULTA_HOY"
    TELECONSULTA = "TELECONSULTA"
    AUTOCUIDADO = "AUTOCUIDADO"


class TriageResult(BaseModel):
    """Resultado del triage. El LLM está OBLIGADO a retornar este formato."""

    nivel: NivelTriage = Field(description="Nivel de urgencia")
    accion: AccionRecomendada = Field(description="Acción concreta a tomar")
    razon: str = Field(description="Justificación breve (max 2 líneas)", max_length=300)
    senales_alarma: list[str] = Field(
        default_factory=list,
        description="Síntomas que motivaron el nivel",
    )
    confianza: float = Field(ge=0.0, le=1.0, description="0.0 a 1.0")
    requiere_medico: bool = Field(
        description="True si se debe escalar a revisión médica humana",
    )
    hospital_sugerido: str | None = Field(
        default=None,
        description="Hospital sugerido si se consultó la herramienta",
    )
    disclaimer: str = Field(
        default="Este resultado NO es un diagnóstico médico. Consulte a un profesional de salud.",
    )


class Protocolo(BaseModel):
    titulo: str
    pasos: list[str]
    fuente: str


class Hospital(BaseModel):
    nombre: str
    distrito: str
    espera_min: int
    capacidad: str
