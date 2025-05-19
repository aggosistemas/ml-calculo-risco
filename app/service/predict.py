import pickle
import logging
import os
import pandas as pd
from fastapi import HTTPException

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Caminho seguro para o modelo
modelo_path = os.path.join(os.path.dirname(__file__), "model.pkl")

# Carregamento do modelo e das colunas
try:
    with open(modelo_path, "rb") as f:
        artefato = pickle.load(f)
        model = artefato["modelo"]
        colunas = artefato["colunas"]
    logger.info("Modelo carregado com sucesso.")
except Exception as e:
    logger.exception("Erro ao carregar o modelo.")
    raise RuntimeError(f"Falha ao carregar o modelo: {e}") from e

# Função principal de predição
def calcular_risco(dados_entrada: dict) -> dict:
    try:
        logger.info(f"Dados recebidos: {dados_entrada}")

        df_entrada = pd.DataFrame([dados_entrada])
        df_entrada = df_entrada[colunas]  # mantém ordem e restrição

        logger.debug(f"DataFrame de entrada: {df_entrada.to_dict()}")

        score = model.predict_proba(df_entrada)[0][1]  # probabilidade classe positiva
        logger.info(f"Score calculado: {score}")

        return {"risco": score}
    except KeyError as ke:
        logger.exception("Chave ausente nos dados de entrada.")
        raise HTTPException(status_code=400, detail=f"Campo obrigatório ausente: {str(ke)}")
    except ValueError as ve:
        logger.exception("Erro de valor.")
        raise HTTPException(status_code=400, detail=f"Erro de valor: {str(ve)}")
    except Exception as e:
        logger.exception("Erro inesperado.")
        raise HTTPException(status_code=500, detail="Erro interno ao calcular risco.")
