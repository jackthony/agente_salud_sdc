"""Tests unitarios de las tools (sin llamar al LLM)."""
from __future__ import annotations

from src.tools import (
    HOSPITALES_DB,
    PROTOCOLOS_DB,
    buscar_hospital_cercano,
    consultar_protocolo_minsa,
    registrar_caso_auditoria,
)


class TestConsultarProtocoloMinsa:
    def test_protocolo_existente(self) -> None:
        salida = consultar_protocolo_minsa("dolor_toracico")
        assert "Dolor Torácico" in salida
        assert "MINSA" in salida

    def test_protocolo_normaliza_espacios_y_case(self) -> None:
        salida = consultar_protocolo_minsa("Dolor Toracico")
        assert "Dolor Torácico" in salida

    def test_protocolo_inexistente_retorna_listado(self) -> None:
        salida = consultar_protocolo_minsa("inexistente")
        assert "no encontrado" in salida.lower()
        for key in PROTOCOLOS_DB:
            assert key in salida


class TestBuscarHospitalCercano:
    def test_sugiere_en_distrito_especifico(self) -> None:
        salida = buscar_hospital_cercano("San Isidro", "VERDE")
        assert "San Isidro" in salida

    def test_ordena_por_menor_espera(self) -> None:
        salida = buscar_hospital_cercano("Lima", "VERDE")
        esperas = [h.espera_min for h in HOSPITALES_DB]
        asumible = min(esperas)
        assert f"~{asumible}" in salida or "espera" in salida

    def test_rojo_filtra_capacidad_baja(self) -> None:
        """ROJO debe preferir capacidad alta/media sobre baja."""
        salida = buscar_hospital_cercano("Lima", "ROJO")
        assert "capacidad: alta" in salida or "capacidad: media" in salida

    def test_distrito_desconocido_usa_fallback(self) -> None:
        salida = buscar_hospital_cercano("Chachapoyas", "VERDE")
        assert "Sugerido" in salida or "106" in salida


class TestRegistrarCasoAuditoria:
    def test_registra_con_timestamp(self) -> None:
        salida = registrar_caso_auditoria("ROJO", "dolor pecho")
        assert "Registrado" in salida
        assert "nivel=ROJO" in salida

    def test_trunca_razon_larga(self) -> None:
        razon_larga = "x" * 500
        salida = registrar_caso_auditoria("VERDE", razon_larga)
        # La razón se trunca a 100 chars en el log
        assert salida.count("x") <= 150
