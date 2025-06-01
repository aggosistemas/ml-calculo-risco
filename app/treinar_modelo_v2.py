import pandas as pd
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split

# Simulação de dataset (substitua pelo seu dataset real)
df = pd.read_csv("dados_simulados_v2.csv")  # você deve ter um arquivo com esses campos

# Colunas de entrada
features = [
    "idade",
    "profissao",
    "renda_mensal",
    "estado_civil",
    "possui_dependentes",
    "valor_cobertura",
    "tipo_cobertura",
    "q01_tem_doenca_grave",
    "q02_fumante",
    "q03_historico_familiar",
    "regra_q01_ativada",
    "regra_q02_ativada",
    "regra_q03_ativada"
]

# Coluna de saída
target = "decisao_final"

# Separação X / y
X = df[features]
y = df[target]

# Colunas categóricas e numéricas
cat_features = ["profissao", "estado_civil", "tipo_cobertura"]
num_features = list(set(features) - set(cat_features))

# Transformadores
transformer = ColumnTransformer(transformers=[
    ("cat", OneHotEncoder(handle_unknown="ignore"), cat_features)
], remainder='passthrough')

# Pipeline
pipeline = Pipeline(steps=[
    ("transformador", transformer),
    ("modelo", RandomForestClassifier(n_estimators=100, random_state=42))
])

# Treinamento
pipeline.fit(X, y)

# Salvando o modelo e as features
with open("model.pkl", "wb") as f:
    pickle.dump({"modelo": pipeline, "colunas": features}, f)

print("Modelo treinado e salvo com sucesso.")
