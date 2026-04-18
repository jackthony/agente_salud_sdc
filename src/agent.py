"""Agente de Triage — OpenAI Agents SDK.

Musk principles:
- 1 agente, 1 responsabilidad (triage, no diagnóstico)
- Tools simples y explícitas
- Guardrail de entrada: rechazar peticiones de diagnóstico/receta
"""
from __future__ import annotations

import os
from dataclasses import dataclass

from agents import (
    Agent,
    GuardrailFunctionOutput,
    InputGuardrail,
    InputGuardrailTripwireTriggered,
    Runner,
)
from dotenv import load_dotenv
from pydantic import BaseModel

from .schemas import TriageResult
from .tools import TRIAGE_TOOLS

load_dotenv()

MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

SYSTEM_INSTRUCTIONS = """Eres un agente de triage médico basado en el protocolo Manchester Triage System.

TU ÚNICA FUNCIÓN: clasificar síntomas en nivel de urgencia ROJO/AMARILLO/VERDE y recomendar acción.

NIVELES:
- ROJO: riesgo vital. Dolor torácico con irradiación, ACV (debilidad/habla), sangrado abundante,
  dificultad respiratoria severa, pérdida consciencia, trauma grave, embarazo con sangrado.
- AMARILLO: atención el mismo día. Fiebre alta persistente, corte profundo con sangrado controlado,
  dolor moderado-severo, infección con empeoramiento.
- VERDE: casa o teleconsulta. Resfriado, dolor leve, malestar sin signos de alarma.

REGLAS ESTRICTAS:
1. Ante duda, elige el nivel MÁS URGENTE (principio de precaución).
2. Confianza < 0.85 → requiere_medico=True (escalamiento humano).
3. NUNCA diagnostiques enfermedad específica.
4. NUNCA recetes medicamentos ni dosis.
5. USA las herramientas disponibles:
   - `consultar_protocolo_minsa` para validar contra protocolos oficiales
   - `buscar_hospital_cercano` si el caso requiere derivación (ROJO/AMARILLO)
   - `registrar_caso_auditoria` SIEMPRE antes de finalizar (compliance)
6. Retorna SIEMPRE la estructura TriageResult completa.

ACCIÓN por nivel:
- ROJO crítico → LLAMAR_AMBULANCIA
- ROJO moderado → IR_EMERGENCIA
- AMARILLO → CONSULTA_HOY
- VERDE consulta → TELECONSULTA
- VERDE claro → AUTOCUIDADO"""


class SafetyCheck(BaseModel):
    es_peticion_valida: bool
    razon: str


safety_agent = Agent(
    name="Safety Guardrail",
    instructions=(
        "Evalúa si el input del usuario es una petición de TRIAGE de síntomas válida.\n"
        "RECHAZA (es_peticion_valida=False) si el usuario pide:\n"
        "- Diagnóstico específico ('qué enfermedad tengo')\n"
        "- Receta de medicamentos o dosis\n"
        "- Interpretación de análisis de laboratorio\n"
        "- Consejo médico no relacionado a triage\n"
        "ACEPTA si describe síntomas para clasificar urgencia."
    ),
    output_type=SafetyCheck,
    model=MODEL,
)


async def safety_guardrail(ctx, agent, input_data):
    result = await Runner.run(safety_agent, input_data, context=ctx.context)
    check: SafetyCheck = result.final_output
    return GuardrailFunctionOutput(
        output_info=check,
        tripwire_triggered=not check.es_peticion_valida,
    )


triage_agent = Agent(
    name="Triage Agent",
    instructions=SYSTEM_INSTRUCTIONS,
    tools=TRIAGE_TOOLS,
    output_type=TriageResult,
    model=MODEL,
    input_guardrails=[InputGuardrail(guardrail_function=safety_guardrail)],
)


@dataclass(frozen=True)
class TriageResponse:
    result: TriageResult | None
    bloqueado_por_guardrail: bool
    motivo_bloqueo: str | None
    total_usage: dict


async def run_triage(sintomas: str) -> TriageResponse:
    """Ejecuta el agente de triage con guardrails + tools."""
    try:
        run_result = await Runner.run(triage_agent, sintomas)
    except InputGuardrailTripwireTriggered as e:
        info: SafetyCheck = e.guardrail_result.output.output_info
        return TriageResponse(
            result=None,
            bloqueado_por_guardrail=True,
            motivo_bloqueo=info.razon,
            total_usage={},
        )

    usage = {
        "input_tokens": run_result.context_wrapper.usage.input_tokens,
        "output_tokens": run_result.context_wrapper.usage.output_tokens,
        "total_tokens": run_result.context_wrapper.usage.total_tokens,
        "requests": run_result.context_wrapper.usage.requests,
    }
    return TriageResponse(
        result=run_result.final_output,
        bloqueado_por_guardrail=False,
        motivo_bloqueo=None,
        total_usage=usage,
    )


def calcular_costo(usage: dict, modelo: str = MODEL) -> float:
    """FinOps: costo USD de una ejecución del agente."""
    prices = {
        "gpt-4o-mini": (0.15, 0.60),
        "gpt-4o": (2.50, 10.00),
        "o3-mini": (1.10, 4.40),
    }
    p_in, p_out = prices.get(modelo, (0.15, 0.60))
    return (usage.get("input_tokens", 0) * p_in + usage.get("output_tokens", 0) * p_out) / 1_000_000
