from fastapi import FastAPI
from app.schemas.request import RiscoRequest
from app.schemas.response import RiscoResponse
from app.service.predict import calcular_risco

app = FastAPI(
    title="API de Cálculo de Risco",
    description="Esta API avalia o risco de um proponente com base em regras de negócio e aprendizado de máquina.",
    version="1.0.0"
)

@app.post("/calcular-risco", response_model=RiscoResponse, summary="Calcular risco do proponente")
def calcular(input_data: RiscoRequest):
    """
    Recebe os dados do proponente e retorna a classificação de risco.
    """
    return calcular_risco(input_data.dict()) 