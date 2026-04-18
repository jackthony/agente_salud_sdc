# Guión Clase 90 min — Agente IA Triage de Síntomas

## Estructura de tiempo

| Min | Bloque | Qué mostrar |
|-----|--------|-------------|
| 0-10 | Problema real | Cola emergencia, datos OMS, Idiot Index |
| 10-20 | Mercado y negocio | Ada Health, Babylon, K Health, números LatAm |
| 20-35 | Arquitectura | Diagrama: Input → Prompt → LLM → Schema → Guardrails |
| 35-75 | Código en vivo | Notebook cell por cell |
| 75-85 | Demo libre | Alumnos dictan casos, el agente responde |
| 85-90 | Cierre | Principios Musk + preguntas |

## Slides (10 máximo)

1. **Título**: Agente IA para Triage — 90 min desde cero
2. **Problema**: Foto cola emergencia + "60% no son emergencias" (OMS)
3. **Idiot Index**: S/150 consulta / S/0.50 tokens = 300x
4. **Donde ya se aplica**: Ada, Babylon, K Health, Infermedica
5. **Modelo negocio**: SaaS B2B, API, White-label — unit economics
6. **Arquitectura** (diagrama simple):
   ```
   Síntomas → System Prompt (Manchester) → gpt-4o-mini → JSON Schema → Guardrails → Respuesta
                                                                          ↓
                                                                   Escalar humano?
   ```
7. **FinOps**: tabla costo gpt-4o-mini vs gpt-4o vs humano
8. **Zero-Hallucination**: 7 técnicas (structured output, disclaimer, etc.)
9. **Demo en vivo** (ir al notebook)
10. **Cierre Musk**: 5 principios aplicados

## Frases clave para cada bloque

### Problema (min 0-10)
- "En Perú hay 1 médico cada 800 habitantes. OMS recomienda 1 cada 500."
- "60% de visitas a emergencia NO son emergencias. La enfermera de triage es el cuello de botella."
- "Idiot Index: el mercado cobra S/150 por consulta. El token cuesta S/0.0005. Ratio 300x."

### Negocio (min 10-20)
- "Ada Health levantó $90M. Babylon llegó a valer $4.2B. El mercado ya validó esto."
- "LatAm digital health: $13.8B en 2024, CAGR 19.8%."
- "Si cobras $0.05 por triage y el costo es $0.00016: margen 99.7%."

### Arquitectura (min 20-35)
- "No es magia. Es prompt + schema + guardrails. Fin."
- "NO usamos RAG. NO fine-tuning. NO vector DB. Musk primero: eliminar."
- "Structured output = el LLM NO PUEDE alucinar el formato."

### Código (min 35-75)
- Ir cell por cell explicando en voz alta
- Mostrar el `usage.prompt_tokens` y calcular costo en vivo
- Poner un caso ambiguo → mostrar escalamiento humano
- Si hay internet-fail: cambiar a Ollama (ya preparado)

### Demo libre (min 75-85)
- Pedir a alumnos que dicten síntomas
- Mostrar latencia + costo de cada call
- Retar al grupo: "intenten que se equivoque"

### Cierre (min 85-90)
- "Construimos un agente real, funcional, validable, en 90 min."
- "Costo de operar: centavos. Valor: triage médico."
- "Próximo paso: validar con 100 casos supervisados. NO automatizar antes."

## Backup plan (si algo falla)

| Falla | Acción |
|-------|--------|
| Sin internet | Usar Ollama local (`USE_LOCAL=True`) |
| API rate limit | Cambiar a casos cacheados (pre-grabados) |
| Error de código | Mostrar versión completa ya ejecutada |
| Proyector muere | README es suficiente para explicar |

## Preguntas esperadas + respuestas cortas

**¿Por qué no usar GPT-4o?**
> 16x más caro, no mejora accuracy en clasificación simple. FinOps gana.

**¿Puede reemplazar al médico?**
> NO. Es triage, no diagnóstico. Es filtro, no decisión final.

**¿Qué pasa si se equivoca?**
> Por eso escalamiento automático si confianza < 0.85, y siempre principio de precaución (elegir el nivel más urgente).

**¿Regulación?**
> Triage no es diagnóstico → menos fricción. Igual se valida con DIGEMID/MINSA antes de producción.

**¿Cómo mejorar el agente?**
> Fine-tuning con casos locales, RAG con protocolos hospitalarios, feedback loop con médicos. PERO: antes de eso, validar.
