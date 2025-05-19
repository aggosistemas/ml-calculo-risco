from pydantic import BaseModel
from typing import Literal


class RiscoResponse(BaseModel):
    score_risco: float
    classificacao_risco: Literal["baixo", "moderado", "alto"]
