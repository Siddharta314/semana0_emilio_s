from pydantic import BaseModel

class Pregunta(BaseModel):
    texto: str = "¿Cuál es la capital de Francia?"

class Respuesta(BaseModel):
    response: str