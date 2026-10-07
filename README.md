# Pre-entrega 3 — Sistema de Recuperación Semántica Local (RAG)

Flujo RAG local con ChromaDB, LangChain (LCEL) y validación estructurada mediante Pydantic.

## Requisitos

- Python 3.12 o superior
- API Key de Google Gemini, OpenAI o Anthropic

## Instalación

1. Crear y activar entorno virtual:
```bash
python -m venv .venv
# En Windows:
.venv\Scripts\Activate.ps1
# En Linux / Mac:
# source .venv/bin/activate
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

3. Configurar variables de entorno:
Crear archivo `.env` a partir de `.env.example`:
```env
LLM_PROVIDER=gemini
GEMINI_API_KEY=tu_clave_de_gemini
# O para OpenAI:
# LLM_PROVIDER=openai
# OPENAI_API_KEY=tu_clave_de_openai
```

## Ejecución

1. Indexar documentos de `data/` en ChromaDB (se ejecuta automáticamente si no existe la base):
```bash
python ingesta.py
```

2. Ejecutar la cadena RAG con las pruebas de validación:
```bash
python main.py
```

## Ejemplo de salida

### Pregunta con respuesta en los documentos:
- **Consulta:** *¿Cual es la politica de retencion de backups y cuando se eliminan definitivamente?*
```json
{
  "respuesta": "La politica de retencion establece que los respaldos pasan los primeros 30 dias en S3 Standard para recuperacion inmediata, de 31 a 365 dias en S3 Glacier Flexible Retrieval para cumplimiento legal y auditoria, y se eliminan definitivamente de forma automatica tras 365 dias.",
  "referencias": [
    "politica_backups.md"
  ]
}
```

### Pregunta trampa (fuera del contexto):
- **Consulta:** *¿Que version de Ruby on Rails y PostgreSQL se usa para la pasarela de pagos?*
```json
{
  "respuesta": "No tengo informacion en el contexto para responder a esta pregunta",
  "referencias": []
}
```
