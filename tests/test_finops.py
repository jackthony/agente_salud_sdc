"""Tests unitarios de FinOps (sin red, sin LLM)."""
from __future__ import annotations

import pytest

from src.agent import calcular_costo


class TestCalcularCosto:
    def test_cero_tokens_cero_costo(self) -> None:
        assert calcular_costo({"input_tokens": 0, "output_tokens": 0}) == 0.0

    def test_gpt_4o_mini_calculo_correcto(self) -> None:
        # 1M input + 1M output con gpt-4o-mini = 0.15 + 0.60 = 0.75
        costo = calcular_costo(
            {"input_tokens": 1_000_000, "output_tokens": 1_000_000},
            modelo="gpt-4o-mini",
        )
        assert costo == pytest.approx(0.75)

    def test_gpt_4o_es_mas_caro_que_mini(self) -> None:
        usage = {"input_tokens": 10_000, "output_tokens": 2_000}
        costo_mini = calcular_costo(usage, modelo="gpt-4o-mini")
        costo_full = calcular_costo(usage, modelo="gpt-4o")
        assert costo_full > costo_mini * 10

    def test_modelo_desconocido_usa_precio_mini(self) -> None:
        usage = {"input_tokens": 100_000, "output_tokens": 50_000}
        costo_desconocido = calcular_costo(usage, modelo="modelo-x")
        costo_mini = calcular_costo(usage, modelo="gpt-4o-mini")
        assert costo_desconocido == costo_mini

    def test_presupuesto_por_triage_bajo_umbral(self) -> None:
        """Un triage típico no debe exceder $0.001 con gpt-4o-mini."""
        # Presupuesto típico: ~2000 tokens in, ~300 out
        costo = calcular_costo(
            {"input_tokens": 2000, "output_tokens": 300},
            modelo="gpt-4o-mini",
        )
        assert costo < 0.001, f"Costo {costo} excede presupuesto FinOps"
