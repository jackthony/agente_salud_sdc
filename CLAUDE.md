# CLAUDE.md — Instrucciones para Asistentes IA

> Este archivo es leído por Claude Code, ChatGPT, Codex, Cursor, y cualquier asistente IA que trabaje en este repo.

## Propósito del Proyecto

Agente de IA que hace **triage de síntomas** (clasificación ROJO/AMARILLO/VERDE + recomendación).
Es material educativo para una clase de 90 minutos sobre agentes IA en salud.

## Reglas Inviolables

### 1. Zero-Hallucination (CRÍTICO)
- **NUNCA** el agente diagnostica enfermedades
- **NUNCA** receta medicamentos ni dosis
- **SIEMPRE** usar structured output (JSON forzado)
- **SIEMPRE** incluir disclaimer: "No es diagnóstico médico"
- **SIEMPRE** escalar a humano si confianza < 0.85

### 2. FinOps (OBLIGATORIO)
- Modelo default: **gpt-4o-mini** ($0.15/$0.60 por 1M tokens)
- `max_tokens=300` máximo
- `temperature=0.1` para consistencia
- Loguear tokens consumidos en cada llamada
- Tener fallback local: **Ollama + Llama 3.2 3B**

### 3. Musk Principles
- Simplificar brutalmente: 1 prompt, 1 modelo, 3 outputs
- Eliminar antes de agregar
- No over-engineer: sin RAG, sin fine-tuning, sin frontend
- Código en UN notebook, no 20 archivos

### 4. Estilo de Código
- Python 3.10+
- Type hints obligatorios
- Immutabilidad: no mutar dicts, retornar copias
- Errores con `raise`, no `except: pass`
- Imports: stdlib → third-party → local

## Stack

| Componente | Tecnología | Por qué |
|-----------|------------|---------|
| LLM principal | OpenAI gpt-4o-mini | Costo/calidad óptimo |
| LLM local (fallback) | Ollama + Llama 3.2 3B | $0, privacidad |
| Entorno | Jupyter Notebook | Demo en vivo |
| Validación | Pydantic | Structured output |
| Env vars | python-dotenv | Gestión de secrets |

## Comandos Clave

```bash
# Setup
pip install -r requirements.txt
cp .env.example .env

# Correr notebook
jupyter notebook notebooks/triage_agent.ipynb

# Correr con Ollama (sin costo)
ollama pull llama3.2:3b
ollama serve
```

## Variables de Entorno

```bash
OPENAI_API_KEY=sk-...       # Requerido si USE_LOCAL=False
USE_LOCAL=False              # True para Ollama
OLLAMA_HOST=http://localhost:11434  # Default
```

## Estructura del Código (un solo notebook)

```
notebooks/triage_agent.ipynb
├── 1. Setup & Imports
├── 2. Config (modelo, temperatura, max_tokens)
├── 3. Schema Pydantic (TriageResult)
├── 4. System Prompt (Manchester Triage)
├── 5. Few-shot Examples
├── 6. Función triage_paciente()
├── 7. Guardrails (validación + escalamiento)
├── 8. Demo: 3 casos (dolor pecho, gripe, corte)
├── 9. Métricas (costo, latencia, tokens)
└── 10. Fallback Ollama (bloque opcional)
```

## Qué NO hacer

- NO usar gpt-4o por defecto (16x más caro que mini)
- NO agregar RAG, fine-tuning, ni vector DB (sobre-ingeniería)
- NO crear múltiples archivos .py (queremos 1 notebook)
- NO poner PII real en los casos de prueba (usar sintéticos)
- NO hacer el agente diagnostique (solo triage)

## Cómo Extender

Si el usuario pide features extras:
1. **Preguntar primero**: ¿realmente lo necesitamos para la clase?
2. **Eliminar antes de agregar**: ¿qué podemos quitar?
3. **Simplificar**: ¿hay forma más simple?
4. Recién ahí implementar

## Para ChatGPT/Codex específicamente

Si eres ChatGPT o Codex y vas a trabajar en este repo:
1. Lee este archivo completo primero
2. Lee el README.md para contexto de negocio
3. No cambies el stack sin consultar
4. Respeta FinOps: usa gpt-4o-mini salvo que haya razón explícita
5. Toda respuesta debe incluir disclaimer médico
6. Si dudas, pregunta en vez de alucinar

## Contacto

- Owner: Tony Aguilar — jaaguilar@acity.com.pe
- Empresa: Neuracode
- Contexto: Material didáctico, clase 90min
