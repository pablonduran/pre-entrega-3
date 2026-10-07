import asyncio
from ingesta import indexar_documentos
from rag import get_rag_response


async def main():
    # Asegura que los documentos esten indexados en ChromaDB
    indexar_documentos()

    consultas = [
        (
            "Prueba 1: Pregunta con respuesta en los documentos",
            "¿Cual es la politica de retencion de backups y cuando se eliminan definitivamente?"
        ),
        (
            "Prueba 2: Pregunta trampa (fuera del contexto)",
            "¿Que version de Ruby on Rails y PostgreSQL se usa para la pasarela de pagos?"
        )
    ]

    for titulo, pregunta in consultas:
        print(f"\n{titulo}")
        print(f"Pregunta: {pregunta}\n")

        resultado = await get_rag_response(pregunta)

        print("Respuesta parseada a Pydantic:")
        print(resultado.model_dump_json(indent=2))


if __name__ == "__main__":
    asyncio.run(main())
