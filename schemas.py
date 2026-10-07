from pydantic import BaseModel, Field


class RespuestaRAG(BaseModel):
    respuesta: str = Field(
        description="Respuesta a la consulta basada exclusivamente en el contexto. Si no hay informacion suficiente en el contexto, debe indicar que no lo sabe."
    )
    referencias: list[str] = Field(
        default_factory=list,
        description="Lista con los nombres o rutas de los documentos de donde se obtuvo la respuesta."
    )
