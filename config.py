import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_anthropic import ChatAnthropic

load_dotenv()

RUTA_VECTORSTORE = Path("./vectorstore")
NOMBRE_COLECCION = "documentos_tecnicos"


def obtener_embeddings():
    proveedor = os.getenv("LLM_PROVIDER", "gemini").lower()

    if proveedor == "gemini":
        clave_api = os.getenv("GEMINI_API_KEY")
        url_base = "https://generativelanguage.googleapis.com/v1beta/openai/"
        modelo = os.getenv("EMBEDDING_MODEL", "gemini-embedding-001")
        return OpenAIEmbeddings(
            model=modelo,
            openai_api_base=url_base,
            openai_api_key=clave_api,
            check_embedding_ctx_length=False,
        )

    clave_api = os.getenv("OPENAI_API_KEY")
    modelo = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
    return OpenAIEmbeddings(model=modelo, api_key=clave_api)


def obtener_llm():
    proveedor = os.getenv("LLM_PROVIDER", "gemini").lower()
    temperatura = float(os.getenv("LLM_TEMPERATURE", "0.0"))

    if proveedor == "anthropic":
        modelo = os.getenv("LLM_MODEL", "claude-3-5-haiku-latest")
        clave_api = os.getenv("ANTHROPIC_API_KEY")
        return ChatAnthropic(model=modelo, api_key=clave_api, temperature=temperatura)

    if proveedor == "gemini":
        modelo = os.getenv("LLM_MODEL", "gemini-3.5-flash-lite")
        clave_api = os.getenv("GEMINI_API_KEY")
        url_base = "https://generativelanguage.googleapis.com/v1beta/openai/"
        return ChatOpenAI(model=modelo, api_key=clave_api, base_url=url_base, temperature=temperatura)

    modelo = os.getenv("LLM_MODEL", "gpt-4o-mini")
    clave_api = os.getenv("OPENAI_API_KEY")
    return ChatOpenAI(model=modelo, api_key=clave_api, temperature=temperatura)
