# app/tests/test_integration_api.py

from fastapi.testclient import TestClient
from app.main import app

# Cria o cliente de testes para a API
client = TestClient(app)

def test_calcular_risco_integration_valido():
    payload = {
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

    response = client.post("/calcular-risco", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "score_risco" in data
    assert "classificacao_risco" in data
    assert isinstance(data["score_risco"], float)
    assert data["classificacao_risco"] in ["baixo", "alto"]


def test_calcular_risco_integration_invalido():
    # Payload com campo faltando ("profissao")
    payload = {
        "idade": 30,
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

    response = client.post("/calcular-risco", json=payload)
    assert response.status_code == 422  # Falha de validação (Unprocessable Entity)

    