"""Fixtures comunes para la suite de tests."""
from __future__ import annotations

import json
from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def casos_prueba() -> list[dict]:
    path = Path(__file__).parent.parent / "data" / "casos_prueba.json"
    return json.loads(path.read_text(encoding="utf-8"))
