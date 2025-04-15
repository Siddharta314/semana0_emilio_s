import os
import ollama
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

#por defecto deepseek-r1
MODELO = os.getenv("MODELO", "deepseek-r1")

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Pregunta(BaseModel):
    texto: str

class Respuesta(BaseModel):
    response: str

@app.post("/preguntar", response_model=Respuesta)
def preguntar(pregunta: Pregunta) -> Respuesta:
    try:
        response = ollama.generate(model=MODELO, prompt=pregunta.texto)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al generar respuesta: {str(e)}"
        )
    if "response" in response:
        return Respuesta(response=response['response'])
    else:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="La respuesta del modelo no contiene la clave 'response'."
        )


@app.get("/modelos" , response_model=list[str])
def listar_modelos() -> list[str]:
    try:
        response = ollama.list()
        model_names = [m["model"] for m in response["models"]]
        return model_names
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al listar modelos: {str(e)}")