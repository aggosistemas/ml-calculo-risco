import pandas as pd
import pickle
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split

# Carrega os dados simulados
df = pd.read_csv("dados_simulados_v2.csv")

# Cria features derivadas
df["cobertura_por_renda"] = df["valor_cobertura"] / df["renda_mensal"]
df["fator_risco_saude"] = (
    df["q01_tem_doenca_grave"].astype(int) +
    df["q02_fumante"].astype(int) +
    df["q03_historico_familiar"].astype(int)
)

# Alvo binário: 1 = risco alto, 0 = risco baixo
df["risco_alto"] = df["decisao_final"].apply(lambda x: 1 if x in ["recusado", "encaminhado"] else 0)

# Define features e target
features = [
    "idade", "profissao", "renda_mensal", "estado_civil", "possui_dependentes",
    "valor_cobertura", "tipo_cobertura", "cobertura_por_renda", "fator_risco_saude",
    "regra_q01_ativada", "regra_q02_ativada", "regra_q03_ativada"
]
target = "risco_alto"

X = df[features]
y = df[target]

# Colunas categóricas
cat_features = ["profissao", "estado_civil", "tipo_cobertura"]
transformer = ColumnTransformer(transformers=[
    ("cat", OneHotEncoder(handle_unknown="ignore"), cat_features)
], remainder='passthrough')

# Pipeline com Logistic Regression e balanceamento de classes
pipeline = Pipeline(steps=[
    ("transformador", transformer),
    ("modelo", LogisticRegression(solver="saga", max_iter=2000, class_weight="balanced", random_state=42))
])

# Treinamento do modelo
pipeline.fit(X, y)

# Salvar modelo e features
with open("model.pkl", "wb") as f:
    pickle.dump({"modelo": pipeline, "colunas": features}, f)

print("Modelo V3 treinado com sucesso e salvo como model.pkl.")
