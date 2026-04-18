"""Tests unitarios de los schemas Pydantic (zero-hallucination)."""
from __future__ import annotations

import pytest
from pydantic import ValidationError

from src.schemas import (
    AccionRecomendada,
    Hospital,
    NivelTriage,
    Protocolo,
    TriageResult,
)


class TestTriageResult:
    def test_construccion_minima_valida(self) -> None:
        r = TriageResult(
            nivel=NivelTriage.VERDE,
            accion=AccionRecomendada.AUTOCUIDADO,
            razon="Cuadro catarral leve",
            confianza=0.9,
            requiere_medico=False,
        )
        assert r.nivel == NivelTriage.VERDE
        assert r.senales_alarma == []
        assert r.hospital_sugerido is None
        assert "NO es un diagnóstico" in r.disclaimer

    def test_disclaimer_siempre_presente(self) -> None:
        r = TriageResult(
            nivel=NivelTriage.ROJO,
            accion=AccionRecomendada.LLAMAR_AMBULANCIA,
            razon="Signos de evento cardiovascular",
            confianza=0.95,
            requiere_medico=True,
        )
        assert r.disclaimer, "Disclaimer es obligatorio siempre"

    @pytest.mark.parametrize("conf_invalida", [-0.1, 1.1, 2.0, -1.0])
    def test_confianza_fuera_de_rango_rechazada(self, conf_invalida: float) -> None:
        with pytest.raises(ValidationError):
            TriageResult(
                nivel=NivelTriage.VERDE,
                accion=AccionRecomendada.AUTOCUIDADO,
                razon="x",
                confianza=conf_invalida,
                requiere_medico=False,
            )

    def test_nivel_invalido_rechazado(self) -> None:
        with pytest.raises(ValidationError):
            TriageResult(
                nivel="MORADO",  # type: ignore[arg-type]
                accion=AccionRecomendada.AUTOCUIDADO,
                razon="x",
                confianza=0.9,
                requiere_medico=False,
            )

    def test_accion_invalida_rechazada(self) -> None:
        with pytest.raises(ValidationError):
            TriageResult(
                nivel=NivelTriage.VERDE,
                accion="RECETAR_PARACETAMOL",  # type: ignore[arg-type]
                razon="x",
                confianza=0.9,
                requiere_medico=False,
            )

    def test_serializacion_json(self) -> None:
        r = TriageResult(
            nivel=NivelTriage.AMARILLO,
            accion=AccionRecomendada.CONSULTA_HOY,
            razon="Fiebre alta persistente",
            senales_alarma=["fiebre >39", "tos productiva"],
            confianza=0.87,
            requiere_medico=False,
        )
        data = r.model_dump()
        assert data["nivel"] == "AMARILLO"
        assert data["accion"] == "CONSULTA_HOY"
        assert data["senales_alarma"] == ["fiebre >39", "tos productiva"]


class TestEnums:
    def test_niveles_triage_son_tres(self) -> None:
        assert {n.value for n in NivelTriage} == {"ROJO", "AMARILLO", "VERDE"}

    def test_acciones_son_cinco(self) -> None:
        esperadas = {
            "LLAMAR_AMBULANCIA",
            "IR_EMERGENCIA",
            "CONSULTA_HOY",
            "TELECONSULTA",
            "AUTOCUIDADO",
        }
        assert {a.value for a in AccionRecomendada} == esperadas


class TestHospitalProtocolo:
    def test_hospital_campos_obligatorios(self) -> None:
        h = Hospital(nombre="X", distrito="Y", espera_min=10, capacidad="alta")
        assert h.espera_min == 10

    def test_protocolo_pasos_lista(self) -> None:
        p = Protocolo(titulo="T", pasos=["a", "b"], fuente="F")
        assert len(p.pasos) == 2
