from pydantic import BaseModel, Field
from typing import Literal


class RiscoRequest(BaseModel):
    idade: int = Field(..., ge=18, le=69)
    profissao: str
    renda_mensal: float = Field(..., ge=0)
    estado_civil: str
    possui_dependentes: bool
    valor_cobertura: float = Field(..., ge=0)
    tipo_cobertura: Literal["morte", "invalidez", "doenca_grave"]
    q01_tem_doenca_grave: bool
    q02_fumante: bool
    q03_historico_familiar: bool
    regra_q01_ativada: bool
    regra_q02_ativada: bool
    regra_q03_ativada: bool
    decisao_final: Literal["aprovado", "recusado", "encaminhado"]
