# Agente IA Salud — Triage de Síntomas (Clase 90min)

> **Caso:** Agente que clasifica síntomas en ROJO/AMARILLO/VERDE y recomienda acción.
> **Enfoque:** Musk + FinOps + Zero-Hallucination.

---

## 1. Caso de Negocio

### Problema real (first principles)
- Emergencias saturadas: 40-60% de visitas son NO-emergencias (OMS)
- Triage manual = enfermera cuello de botella (costo S/50/hora)
- Pacientes esperan 4-8h por casos que pudieron ser teleconsulta

### Dónde ya se aplica (referencias reales)
| Empresa | País | Valor |
|---------|------|-------|
| **Ada Health** | Alemania | 13M usuarios, levantó $90M Serie B |
| **Babylon Health** | UK | NHS contract, IPO $4.2B (2021) |
| **K Health** | USA/Israel | $8.9M ARR, partnership Mayo Clinic |
| **Buoy Health** | USA | Harvard Med spin-off, partnerships con CVS |
| **Infermedica** | Polonia | API B2B, usado por Allianz, PZU |

### Por qué es bueno hacerlo
- Problema **masivo y medible** (tiempo de espera, costo por paciente)
- Solución **ya validada** por mercado ($2B+ invertido en el sector)
- Tecnología **commodity** (LLMs) → barrera de entrada baja
- Regulación clara (no diagnóstico, solo triage → menos fricción FDA/DIGEMID)

---

## 2. Modelo de Negocio

### Cómo ganar dinero
1. **SaaS B2B a clínicas/EPS**: S/2,000-10,000/mes por sede
2. **API pay-per-call**: $0.05/triage (margen 300x sobre costo LLM)
3. **White-label** a aseguradoras (Pacífico, Rimac, Mapfre)
4. **Integración farmacias** (Inkafarma, MiFarma) → comisión derivación
5. **Data insights** agregados a MINSA/EsSalud (no PII)

### Demanda (Perú + LatAm)
- Perú: 33M habitantes, 1 médico/800 hab (OMS recomienda 1/500)
- LatAm digital health: **$13.8B en 2024**, CAGR 19.8% (Statista)
- Post-COVID: telemedicina creció 38x en Perú (SUSALUD 2023)
- Clínicas privadas buscan diferenciación digital

### Unit Economics (del caso base)
- Costo por triage: **$0.00016** (gpt-4o-mini)
- Precio sugerido: **$0.05/call** o **S/1.50/triage**
- Margen bruto: **99.7%**
- Break-even: ~200 triages/mes por cliente

---

## 3. Velocidad de Implementación (Musk-mode)

| Fase | Tiempo | Qué sale |
|------|--------|----------|
| MVP demo | **90 min** (esta clase) | Notebook funcional |
| Piloto 1 clínica | **2 semanas** | API + WhatsApp bot |
| Producción SaaS | **2 meses** | Dashboard + multi-tenant |
| Escalamiento | **6 meses** | 10+ clínicas, integración HIS |

### Algoritmo Musk aplicado
1. **Cuestionar**: ¿necesitamos RAG? NO. ¿Fine-tuning? NO. ¿UI compleja? NO.
2. **Eliminar**: sin frontend, sin DB, sin auth (es clase)
3. **Simplificar**: 1 prompt + 1 modelo + 3 outputs
4. **Acelerar**: Jupyter → demo en vivo → feedback
5. **Automatizar**: solo después de validar 100 casos manuales

---

## 4. FinOps

### Modelo elegido: **gpt-4o-mini**
| Modelo | Input/1M | Output/1M | Por triage |
|--------|----------|-----------|------------|
| gpt-4o-mini | $0.15 | $0.60 | **$0.00016** |
| gpt-4o | $2.50 | $10.00 | $0.0027 (16x más) |
| o3-mini | $1.10 | $4.40 | $0.0012 |

### Fallback local (sin costo)
- **Ollama + Llama 3.2 3B** → $0 por triage
- Usar si: privacidad estricta, offline, o budget $0
- Ver sección `Modelo Local` en notebook

### Guardrails de costo
- `max_tokens=300` (respuesta corta)
- `temperature=0.1` (consistencia)
- Timeout 10s
- Contador de tokens por llamada

---

## 5. Zero-Hallucination

### Técnicas aplicadas
1. **Structured Output** (JSON Schema forzado) — no puede inventar formato
2. **Few-shot prompting** — 3 ejemplos calibrados
3. **Protocolo Manchester Triage** en system prompt
4. **Disclaimer obligatorio**: "No es diagnóstico médico"
5. **Escalamiento humano** si confianza < 0.85
6. **Lista blanca de acciones** — solo puede recomendar de un set fijo
7. **Auditoría**: cada decisión se loguea con timestamp + prompt + respuesta

### Lo que el agente NUNCA hace
- Diagnosticar enfermedades
- Recetar medicamentos
- Dar dosis
- Reemplazar consulta médica

---

## 6. Setup (para ChatGPT/Codex/Claude/cualquiera)

### Requisitos
- Python 3.10+
- Jupyter Notebook
- API key OpenAI (opcional, puede correr con Ollama local)

### Instalación
```bash
git clone <repo-url>
cd agente_salud_sdc
pip install -r requirements.txt
cp .env.example .env
# Editar .env con tu OPENAI_API_KEY
jupyter notebook notebooks/triage_agent.ipynb
```

### Correr sin OpenAI (100% local)
```bash
# Instalar Ollama: https://ollama.com
ollama pull llama3.2:3b
# En el notebook, cambiar flag USE_LOCAL=True
```

---

## 7. Estructura del Repo

```
agente_salud_sdc/
├── README.md              # Este archivo (caso de negocio + setup)
├── CLAUDE.md              # Instrucciones para asistentes IA
├── requirements.txt       # Dependencias Python
├── .env.example           # Template de variables
├── notebooks/
│   └── triage_agent.ipynb # Código principal (clase)
├── data/
│   └── casos_prueba.json  # Casos de test
└── slides/
    └── guion.md           # Guión de la clase (90 min)
```

---

## 8. Créditos y Licencia

- Autor: Tony Aguilar (CEO Neuracode)
- Clase: Agentes IA para Salud
- Licencia: MIT
- Disclaimer: Material educativo. No usar en producción sin validación médica.
