"""CLI interactivo — demo en vivo del agente.

Uso:
    python cli.py             # modo interactivo
    python cli.py --casos     # corre suite de casos de prueba
"""
from __future__ import annotations

import argparse
import asyncio
import json
import time
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from src.agent import calcular_costo, run_triage

console = Console()


def _render_resultado(sintomas: str, response, latencia_s: float) -> None:
    if response.bloqueado_por_guardrail:
        console.print(
            Panel.fit(
                f"[yellow]Petición fuera de alcance[/yellow]\n[dim]{response.motivo_bloqueo}[/dim]",
                title="BLOQUEADO por guardrail",
                border_style="yellow",
            )
        )
        return

    r = response.result
    color = {"ROJO": "red", "AMARILLO": "yellow", "VERDE": "green"}[r.nivel.value]

    cuerpo = (
        f"[bold {color}]NIVEL: {r.nivel.value}[/bold {color}]\n"
        f"Acción: [bold]{r.accion.value}[/bold]\n"
        f"Razón: {r.razon}\n"
        f"Señales alarma: {', '.join(r.senales_alarma) or '(ninguna)'}\n"
        f"Confianza: {r.confianza:.2f}\n"
        f"Escalar a médico: [bold]{'SÍ' if r.requiere_medico else 'no'}[/bold]\n"
    )
    if r.hospital_sugerido:
        cuerpo += f"Hospital: {r.hospital_sugerido}\n"
    cuerpo += f"\n[dim]{r.disclaimer}[/dim]"

    console.print(Panel(cuerpo, title=f"Triage — {sintomas[:60]}", border_style=color))

    u = response.total_usage
    costo = calcular_costo(u)
    console.print(
        f"[dim]FinOps: {u['requests']} requests · "
        f"{u['input_tokens']} in + {u['output_tokens']} out tokens · "
        f"${costo:.6f} · {latencia_s:.2f}s[/dim]\n"
    )


async def correr_interactivo() -> None:
    console.print(
        Panel.fit(
            "[bold]Agente de Triage de Síntomas[/bold]\n"
            "Describe los síntomas del paciente. Escribe 'salir' para terminar.\n"
            "[dim]No es diagnóstico. Solo clasifica urgencia.[/dim]",
            border_style="cyan",
        )
    )
    while True:
        sintomas = console.input("[bold cyan]Síntomas>[/bold cyan] ").strip()
        if sintomas.lower() in ("salir", "exit", "quit", ""):
            break
        t0 = time.time()
        response = await run_triage(sintomas)
        _render_resultado(sintomas, response, time.time() - t0)


async def correr_casos_prueba() -> None:
    path = Path(__file__).parent / "data" / "casos_prueba.json"
    casos = json.loads(path.read_text(encoding="utf-8"))

    tabla = Table(title="Suite de Casos de Prueba")
    tabla.add_column("ID")
    tabla.add_column("Esperado")
    tabla.add_column("Predicho")
    tabla.add_column("Conf")
    tabla.add_column("Escalar")
    tabla.add_column("Tokens")
    tabla.add_column("Costo $")
    tabla.add_column("Lat s")
    tabla.add_column("OK")

    aciertos = 0
    costo_total = 0.0
    for c in casos:
        t0 = time.time()
        response = await run_triage(c["descripcion"])
        lat = time.time() - t0

        if response.bloqueado_por_guardrail or response.result is None:
            tabla.add_row(c["id"], c["esperado"], "BLOQUEADO", "-", "-", "-", "-", f"{lat:.2f}", "✗")
            continue

        r = response.result
        costo = calcular_costo(response.total_usage)
        costo_total += costo
        ok = r.nivel.value == c["esperado"]
        aciertos += int(ok)
        tabla.add_row(
            c["id"],
            c["esperado"],
            r.nivel.value,
            f"{r.confianza:.2f}",
            "SI" if r.requiere_medico else "no",
            f"{response.total_usage['input_tokens']}+{response.total_usage['output_tokens']}",
            f"{costo:.6f}",
            f"{lat:.2f}",
            "✓" if ok else "✗",
        )

    console.print(tabla)
    n = len(casos)
    console.print(f"\n[bold]Accuracy:[/bold] {aciertos}/{n} = {aciertos/n*100:.1f}%")
    console.print(f"[bold]Costo total:[/bold] ${costo_total:.6f}")
    console.print(f"[bold]Costo promedio:[/bold] ${costo_total/n:.6f}/caso")


def main() -> None:
    parser = argparse.ArgumentParser(description="Agente IA Triage de Síntomas")
    parser.add_argument("--casos", action="store_true", help="Correr suite de casos de prueba")
    args = parser.parse_args()

    if args.casos:
        asyncio.run(correr_casos_prueba())
    else:
        asyncio.run(correr_interactivo())


if __name__ == "__main__":
    main()
