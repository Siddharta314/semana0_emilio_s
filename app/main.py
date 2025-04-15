import ollama
import logging
from fastapi import HTTPException, status
from .app import create_app
from .config import settings
from .schemas import Pregunta, Respuesta

app = create_app()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)


@app.post(
    "/preguntar",
    response_model=Respuesta,
    summary="Realiza una pregunta al modelo",
    description="Envía una pregunta al modelo seleccionado y recibe una respuesta generada."
)
def preguntar(pregunta: Pregunta) -> Respuesta:
    if not pregunta.texto or not pregunta.texto.strip():
        raise HTTPException(
            status_code=400,
            detail="La pregunta no puede estar vacía."
        )
    logging.info(f"Pregunta recibida: {pregunta.texto}")
    try:
        response = ollama.generate(model=settings.MODELO, prompt=pregunta.texto)
    except Exception as e:
        logging.error(f"Error al generar respuesta: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al generar respuesta: {str(e)}"
        )
    if "response" in response:
        logging.info("Respuesta generada correctamente.")
        return Respuesta(response=response['response'])
    else:
        logging.error("La respuesta del modelo no contiene la clave 'response'.")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="La respuesta del modelo no contiene la clave 'response'."
        )


@app.get(
    "/modelos",
    response_model=list[str],
    summary="Lista los modelos disponibles",
    description="Devuelve una lista con los nombres de los modelos disponibles en Ollama."
)
def listar_modelos() -> list[str]:
    try:
        response = ollama.list()
        model_names = [m["model"] for m in response["models"]]
        return model_names
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al listar modelos: {str(e)}")


@app.get(
    "/",
    summary="Información de la API",
    description="Muestra información básica sobre la API."
)
def root() -> dict[str, str]:
    return {
        "mensaje": "API de preguntas a modelos Ollama. Usa /preguntar para interactuar y /modelos para ver los modelos disponibles."
    }
