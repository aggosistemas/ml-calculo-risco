# app/tests/test_predict.py
import pytest
from app.service.predict import calcular_risco


def test_calcular_risco_basico():
    entrada_valida = {
        "idade": 30,
        "profissao": "Engenheiro",
        "renda_mensal": 5000.0,
        "estado_civil": "solteiro",
        "possui_dependentes": False,
        "valor_cobertura": 200000.0,
        "tipo_cobertura": "morte",
        "q01_tem_doenca_grave": False,
        "q02_fumante": False,
        "q03_historico_familiar": False,
        "regra_q01_ativada": True,
        "regra_q02_ativada": True,
        "regra_q03_ativada": False
    }

    resultado = calcular_risco(entrada_valida)
    assert "score_risco" in resultado
    assert "classificacao_risco" in resultado
    assert isinstance(resultado["score_risco"], float)
    assert resultado["classificacao_risco"] in ["baixo", "alto"]


def test_calcular_risco_campos_faltando():
    entrada_invalida = {
        "idade": 30,
        # campo "profissao" faltando
        "renda_mensal": 5000.0,
        "estado_civil": "solteiro",
        "possui_dependentes": False,
        "valor_cobertura": 200000.0,
        "tipo_cobertura": "morte",
        "q01_tem_doenca_grave": False,
        "q02_fumante": False,
        "q03_historico_familiar": False,
        "regra_q01_ativada": True,
        "regra_q02_ativada": True,
        "regra_q03_ativada": False
    }

    with pytest.raises(Exception):
        calcular_risco(entrada_invalida)
