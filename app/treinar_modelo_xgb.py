import pandas as pd
import pickle
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from xgboost import XGBClassifier

# Carrega os dados
df = pd.read_csv("dados_simulados_v3.csv")

# Features derivadas
df["cobertura_por_renda"] = df["valor_cobertura"] / df["renda_mensal"]
df["fator_risco_saude"] = (
    df["q01_tem_doenca_grave"].astype(int) +
    df["q02_fumante"].astype(int) +
    df["q03_historico_familiar"].astype(int)
)

# Alvo e features
features = ['idade', 'profissao', 'renda_mensal', 'estado_civil', 'possui_dependentes', 'valor_cobertura', 'tipo_cobertura', 'cobertura_por_renda', 'fator_risco_saude', 'regra_q01_ativada', 'regra_q02_ativada', 'regra_q03_ativada']
target = "risco_alto"
X = df[features]
y = df[target]

# Transformações
cat_features = ['profissao', 'estado_civil', 'tipo_cobertura']
transformer = ColumnTransformer(transformers=[
    ("cat", OneHotEncoder(handle_unknown="ignore"), cat_features)
], remainder="passthrough")

# Modelo
xgb_model = XGBClassifier(use_label_encoder=False, eval_metric="logloss", scale_pos_weight=1.5, random_state=42)

pipeline = Pipeline(steps=[
    ("transformador", transformer),
    ("modelo", xgb_model)
])

# Treinamento
pipeline.fit(X, y)

# Salvar modelo
with open("model.pkl", "wb") as f:
    pickle.dump({"modelo": pipeline, "colunas": features}, f)

print("Modelo XGBoost treinado e salvo como model.pkl")
