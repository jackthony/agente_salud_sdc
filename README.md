# Agente IA Salud — Triage de Síntomas (Clase 90min)

> **Agente real** con OpenAI Agents SDK. Tool use + guardrails + structured output.
> **Enfoque:** Minimalismo + FinOps + Zero-Hallucination.
>
> 🎓 **Clase dictada para [SDC Learning](https://www.sdclearning.com/)** · Docente: Jack Aguilar — CEO Neuracode

---

## 1. Caso de Negocio

### Problema real (first principles)
- Emergencias saturadas: 40-60% de visitas son NO-emergencias (OMS)
- Triage manual = enfermera cuello de botella (~S/50/hora)
- Pacientes esperan 4-8h por casos que pudieron ser teleconsulta

### Dónde ya se aplica (referencias reales)
| Empresa | País | Valor |
|---------|------|-------|
| **Ada Health** | Alemania | 13M usuarios, Serie B $90M |
| **Babylon Health** | UK | Contrato NHS, IPO $4.2B (2021) |
| **K Health** | USA/Israel | Partnership Mayo Clinic |
| **Buoy Health** | USA | Spin-off Harvard Med |
| **Infermedica** | Polonia | API B2B, Allianz, PZU |

### Modelo de negocio
1. SaaS B2B clínicas/EPS: S/2,000-10,000/mes por sede
2. API pay-per-call: $0.05/triage (margen 99.7%)
3. White-label aseguradoras (Pacífico, Rimac)
4. Comisión derivación farmacia (Inkafarma, MiFarma)

### Unit Economics
- Costo por triage: **~$0.0003** (gpt-4o-mini, incluye tool calls)
- Precio sugerido: **$0.05**
- Break-even: ~200 triages/mes por cliente

---

## 2. Qué es un Agente (vs simple LLM)

| Capacidad | LLM wrapper | **Agente real (este repo)** |
|-----------|------------|------------------------------|
| Clasificar | sí | sí |
| Tool use (APIs, DB) | no | **sí** (protocolos MINSA, hospitales, auditoría) |
| Loop autónomo de decisión | no | **sí** (el agente decide qué tools llamar) |
| Guardrails | manual | **nativos** (rechaza diagnóstico/recetas) |
| Structured output | parcial | **garantizado** (Pydantic schema) |

Stack: **OpenAI Agents SDK** (oficial, marzo 2025) + Pydantic + Rich.

---

## 3. Zero-Hallucination

| Técnica | Cómo |
|---------|------|
| Structured output | Pydantic `TriageResult` obligatorio |
| Protocolos oficiales | Tool `consultar_protocolo_minsa` |
| Guardrail de entrada | Safety agent rechaza diagnóstico/recetas |
| Escalamiento humano | `requiere_medico=True` si confianza < 0.85 |
| Disclaimer | incluido en cada respuesta |
| Auditoría | Tool `registrar_caso_auditoria` obligatoria |
| Lista blanca de acciones | solo 5 acciones posibles (enum) |

---

## 4. FinOps

### Modelo default: **gpt-4o-mini**
| Modelo | Input/1M | Output/1M |
|--------|----------|-----------|
| gpt-4o-mini | $0.15 | $0.60 |
| gpt-4o | $2.50 | $10.00 (16x) |

Guardrails: `max_tokens=300`, `temperature=0.1`, timeout 10s.

---

## 5. Setup (ChatGPT / Codex / Claude / cualquiera)

### Requisitos
- Python 3.10+
- API key OpenAI

### Instalación (recomendado: venv aislado)
```bash
git clone https://github.com/jackthony/agente_salud_sdc
cd agente_salud_sdc

# Crear entorno virtual
python -m venv .venv
# Activar (Windows bash/git-bash):
source .venv/Scripts/activate
# Activar (Windows PowerShell):
# .venv\Scripts\Activate.ps1
# Activar (macOS/Linux):
# source .venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt       # core (para correr el agente)
pip install -r requirements-dev.txt   # opcional: pytest + jupyter

# Configurar API key
cp .env.example .env
# Editar .env con tu OPENAI_API_KEY
```

### Uso

**Modo interactivo (CLI):**
```bash
python cli.py
```

**Suite de pruebas:**
```bash
python cli.py --casos
```

**Notebook demo (para clase):**
```bash
jupyter notebook demo.ipynb
```

### Tests

```bash
# Unitarios (rápidos, sin gastar tokens)
pytest

# Integración (llama al LLM real, requiere OPENAI_API_KEY)
pytest -m integration
```

---

## 6. Estructura

```
agente_salud_sdc/
├── README.md              # Caso de negocio + setup
├── CLAUDE.md              # Instrucciones para asistentes IA
├── requirements.txt
├── .env.example
├── cli.py                 # CLI interactivo + suite de pruebas
├── demo.ipynb             # Notebook demo para clase
├── src/
│   ├── schemas.py         # Pydantic: TriageResult, Hospital, Protocolo
│   ├── tools.py           # Tools: protocolo MINSA, hospital, auditoría
│   └── agent.py           # Agente principal + safety guardrail
├── data/
│   └── casos_prueba.json  # 7 casos de test (ROJO/AMARILLO/VERDE)
└── slides/
    └── guion.md           # Guión de clase 90min
```

---

## 7. Principios de Diseño

| Principio | Cómo |
|-----------|------|
| **Cuestionar** | ¿RAG? NO. ¿Fine-tuning? NO. ¿Frontend? NO. |
| **Eliminar** | 3 archivos `.py`, 1 notebook demo. Cero sobra. |
| **Simplificar** | 1 agente principal + 1 guardrail + 3 tools. |
| **Acelerar** | 90 min clase → agente completo + métricas. |
| **Automatizar al final** | Solo después de validar con médicos reales. |

---

## 8. Autor y Contacto

**Jack Aguilar** — CEO Neuracode

- 🌐 Web: [neuracode.dev](https://www.neuracode.dev/)
- 💼 LinkedIn: [linkedin.com/in/jackaguilarc](https://www.linkedin.com/in/jackaguilarc/)
- 🎵 TikTok: [@jack.de.neura.code](https://www.tiktok.com/@jack.de.neura.code)
- 📸 Instagram: [@neuracode.dev](https://www.instagram.com/neuracode.dev/)
- 📘 Facebook: [facebook.com/neuracode](https://www.facebook.com/neuracode)
- 💬 WhatsApp: [+51 982 859 073](https://wa.me/51982859073)
- 📧 Email: jaaguilar@acity.com.pe

---

## 9. Licencia y Disclaimer

- **Licencia:** MIT
- **Disclaimer:** Material educativo. No usar en producción sin validación médica y aprobación regulatoria (DIGEMID / MINSA).
