import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Carregar os dados
df = pd.read_csv("dados.csv")

# Variáveis derivadas
df["decisao_bin"] = df["decisao_final"].map({
    "aprovado": 0,
    "recusado": 1,
    "encaminhado": 1
})
df["fumante_bin"] = df["q02_fumante"].astype(int)
df["cobertura_por_renda"] = df["valor_cobertura"] / df["renda_mensal"]

# Correlação entre numéricas e risco
print("\n--- Correlação numérica ---")
print(df[["idade", "renda_mensal", "valor_cobertura", "cobertura_por_renda", "decisao_bin"]].corr())

# Scatterplot: cobertura vs renda por decisão
sns.scatterplot(data=df, x="renda_mensal", y="valor_cobertura", hue="decisao_final")
plt.title("Cobertura vs Renda por decisão")
plt.xlabel("Renda Mensal")
plt.ylabel("Valor de Cobertura")
plt.grid(True)
plt.tight_layout()
plt.show()

# Boxplot: idade × fumante × decisão
sns.boxplot(data=df, x="q02_fumante", y="idade", hue="decisao_final")
plt.title("Distribuição de idade por fumante e decisão")
plt.tight_layout()
plt.show()

# Risco médio por perfil fumante
print("\n--- Risco médio por fumante ---")
print(df.groupby("q02_fumante")["decisao_bin"].mean())
