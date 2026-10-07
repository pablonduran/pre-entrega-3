import os
from pathlib import Path
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma

from config import RUTA_VECTORSTORE, NOMBRE_COLECCION, obtener_embeddings

CARPETA_DATA = Path("./data")


def cargar_documentos() -> list[Document]:
    documentos = []
    for ruta_archivo in CARPETA_DATA.glob("*"):
        if ruta_archivo.suffix.lower() in [".txt", ".md"]:
            with open(ruta_archivo, "r", encoding="utf-8") as f:
                contenido = f.read()
            documentos.append(
                Document(
                    page_content=contenido,
                    metadata={"fuente": ruta_archivo.name}
                )
            )
    return documentos


def indexar_documentos(forzar: bool = False):
    embeddings = obtener_embeddings()

    vectorstore = Chroma(
        collection_name=NOMBRE_COLECCION,
        persist_directory=str(RUTA_VECTORSTORE),
        embedding_function=embeddings,
    )

    cantidad_actual = vectorstore._collection.count()
    if cantidad_actual > 0 and not forzar:
        print(f"La base vectorial ya contiene {cantidad_actual} fragmentos. Se omite la indexacion.")
        return vectorstore

    if forzar and cantidad_actual > 0:
        print("Limpiando coleccion existente...")
        vectorstore.reset_collection()

    documentos = cargar_documentos()
    if not documentos:
        print("No se encontraron documentos en la carpeta data/.")
        return vectorstore

    divisor = RecursiveCharacterTextSplitter(
        chunk_size=700,
        chunk_overlap=100,
        separators=["\n\n", "\n", " ", ""]
    )
    fragmentos = divisor.split_documents(documentos)

    print(f"Indexando {len(fragmentos)} fragmentos en ChromaDB...")
    vectorstore.add_documents(fragmentos)
    print("Indexacion completada exitosamente.")
    return vectorstore


if __name__ == "__main__":
    indexar_documentos()
