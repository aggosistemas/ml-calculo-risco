import pickle
import logging
import os
import pandas as pd
from fastapi import HTTPException

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Caminho seguro para o modelo
#modelo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "model", "modelo_xgb_revisado.pkl"))
modelo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "model", "model.pkl"))




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
        # Adiciona features derivadas
        df_entrada["cobertura_por_renda"] = df_entrada["valor_cobertura"] / df_entrada["renda_mensal"]
        df_entrada["fator_risco_saude"] = (
            df_entrada["q01_tem_doenca_grave"].astype(int) +
            df_entrada["q02_fumante"].astype(int) +
            df_entrada["q03_historico_familiar"].astype(int)
        )

        # Mantém ordem e restrição
        df_entrada = df_entrada[colunas]

        logger.debug(f"DataFrame de entrada: {df_entrada.to_dict()}")

        score = model.predict_proba(df_entrada)[0][1]  # probabilidade classe positiva
        logger.info(f"Score calculado: {score}")

        return {
                 "score_risco": float(score),
                    "classificacao_risco": "baixo" if score < 0.5 else "alto"
                }       
    except KeyError as ke:
        logger.exception("Chave ausente nos dados de entrada.")
        raise HTTPException(status_code=400, detail=f"Campo obrigatório ausente: {str(ke)}")
    except ValueError as ve:
        logger.exception("Erro de valor.")
        raise HTTPException(status_code=400, detail=f"Erro de valor: {str(ve)}")
    except Exception as e:
        logger.exception("Erro inesperado.")
        raise HTTPException(status_code=500, detail="Erro interno ao calcular risco.")
