# CLAUDE.md — Instrucciones para Asistentes IA

> Leído por Claude Code, ChatGPT, Codex, Cursor, y cualquier asistente IA que trabaje en este repo.

## Propósito

Agente de IA (no solo LLM wrapper) que hace **triage de síntomas**: clasifica en ROJO/AMARILLO/VERDE, recomienda acción, usa tools para consultar protocolos MINSA y sugerir hospital. Material educativo para clase de 90 min.

## Stack

- **OpenAI Agents SDK** (`openai-agents`, oficial marzo 2025)
- **Python 3.10+**
- **Pydantic 2** para structured output
- **Rich** para CLI bonito
- **Jupyter** solo para demo final

## Reglas Inviolables

### 1. Zero-Hallucination (CRÍTICO)
- El agente NUNCA diagnostica enfermedades
- El agente NUNCA receta medicamentos ni dosis
- Structured output obligatorio (`TriageResult` Pydantic)
- Safety guardrail de entrada que rechaza pedidos fuera de alcance
- Escalamiento humano automático si `confianza < 0.85`
- Disclaimer en cada respuesta

### 2. FinOps (OBLIGATORIO)
- Modelo default: **`gpt-4o-mini`** (NO usar gpt-4o salvo razón explícita)
- Tracing automático del SDK → ver tokens y costo
- Presupuesto: < $0.001 por triage

### 3. Musk Principles
- 1 agente = 1 responsabilidad (triage, NO diagnóstico)
- Eliminar antes de agregar (no RAG, no fine-tuning, no frontend)
- Código mínimo: `src/agent.py` + `src/tools.py` + `src/schemas.py`
- CLI directo, notebook solo para métricas

### 4. Estilo de Código
- Python 3.10+ (`|` para unions, `list[X]` en vez de `List[X]`)
- Type hints obligatorios en todas las funciones
- Immutabilidad: `@dataclass(frozen=True)`, retornar copias
- Errores con `raise`, nunca `except: pass`
- Imports: stdlib → third-party → local (separados por línea vacía)

## Estructura del Código

```
src/
├── schemas.py   # Pydantic: TriageResult, Hospital, Protocolo (NO LLM)
├── tools.py     # @function_tool decorados (protocolos, hospitales, auditoría)
└── agent.py     # Agente + safety guardrail + run_triage() async
cli.py           # Entrada: interactivo o --casos
demo.ipynb       # Métricas finops para clase
```

## Comandos

```bash
# Setup
pip install -r requirements.txt
cp .env.example .env  # editar OPENAI_API_KEY

# Correr
python cli.py              # modo interactivo
python cli.py --casos      # suite de pruebas
jupyter notebook demo.ipynb
```

## Variables de Entorno

```bash
OPENAI_API_KEY=sk-...        # requerido
OPENAI_MODEL=gpt-4o-mini     # default FinOps, no cambiar sin razón
```

## Conceptos del OpenAI Agents SDK

| Concepto | Rol |
|----------|-----|
| `Agent` | Configuración: instructions + tools + output_type + guardrails |
| `@function_tool` | Decorator que expone funciones Python como tools al LLM |
| `Runner.run()` | Ejecuta el loop del agente (percibir → decidir → act → observar) |
| `InputGuardrail` | Valida input ANTES de llamar al agente principal |
| `output_type` | Fuerza structured output con Pydantic |
| `ContextWrapper.usage` | Tokens + requests para FinOps |

## Qué NO hacer

- NO usar gpt-4o por defecto (16x más caro)
- NO agregar LangChain, CrewAI, LlamaIndex (conflicto con SDK oficial)
- NO agregar RAG/vector DB (sobre-ingeniería)
- NO remover el safety guardrail
- NO remover el disclaimer
- NO poner PII real en casos de prueba
- NO hacer que el agente diagnostique enfermedades específicas
- NO dividir en más archivos sin razón (keep it simple)

## Para ChatGPT / Codex específicamente

Si eres ChatGPT o Codex:
1. Lee este archivo + README.md primero
2. Usa el SDK oficial `openai-agents`, no reinventes con LangChain
3. Respeta FinOps: `gpt-4o-mini` salvo razón explícita
4. Cualquier cambio al agente debe mantener los guardrails
5. Si dudas, pregunta en vez de alucinar código

## Cómo Extender (si se pide)

Antes de implementar, preguntar:
1. ¿Realmente lo necesitamos para la clase / caso de negocio?
2. ¿Qué podemos eliminar primero?
3. ¿Hay forma más simple?

Extensiones válidas (en orden de prioridad):
- Más tools (historial paciente, teleconsulta, farmacia cercana)
- Handoff a agente especialista (pediatría, cardiología) — nativo en el SDK
- Memoria persistente (SQLite) para aprendizaje por casos
- Streaming de respuestas

## Contacto

- Owner: Tony Aguilar — jaaguilar@acity.com.pe
- Empresa: Neuracode
- Repo: https://github.com/jackthony/agente_salud_sdc
