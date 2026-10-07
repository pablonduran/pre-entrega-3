from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_chroma import Chroma

from config import RUTA_VECTORSTORE, NOMBRE_COLECCION, obtener_embeddings, obtener_llm
from schemas import RespuestaRAG


def formatear_documentos(documentos) -> str:
    bloques = []
    for doc in documentos:
        fuente = doc.metadata.get("fuente", "desconocido")
        bloques.append(f"[Documento: {fuente}]\n{doc.page_content}")
    return "\n\n".join(bloques)


vectorstore = Chroma(
    collection_name=NOMBRE_COLECCION,
    persist_directory=str(RUTA_VECTORSTORE),
    embedding_function=obtener_embeddings(),
)

recuperador = vectorstore.as_retriever(search_kwargs={"k": 3})

plantilla_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "Sos un asistente tecnico. Responde a la pregunta del usuario utilizando "
        "EXCLUSIVAMENTE la informacion contenida en el siguiente contexto.\n\n"
        "Reglas obligatorias:\n"
        "1. Si la respuesta no esta en el contexto, di claramente: 'No tengo informacion en el contexto para responder a esta pregunta'.\n"
        "2. No utilices conocimiento externo ni inventes datos.\n"
        "3. En el campo 'referencias', indica los nombres de los archivos fuente usados para responder. Si no sabes la respuesta o no esta en el contexto, deja la lista vacia.\n"
        "4. Responde siempre en texto plano continuo, sin asteriscos ni negritas de markdown.\n\n"
        "Contexto:\n{contexto}"
    ),
    ("human", "{pregunta}")
])

modelo = obtener_llm()
modelo_estructurado = modelo.with_structured_output(RespuestaRAG)

cadena_rag = (
    {
        "contexto": recuperador | formatear_documentos,
        "pregunta": RunnablePassthrough()
    }
    | plantilla_prompt
    | modelo_estructurado
).with_retry(stop_after_attempt=3)


async def get_rag_response(query: str) -> RespuestaRAG:
    if not query or not query.strip():
        raise ValueError("La consulta no puede estar vacia.")

    resultado = await cadena_rag.ainvoke(query)
    return resultado


obtener_respuesta_rag = get_rag_response
