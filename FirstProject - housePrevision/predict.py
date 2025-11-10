import pandas as pd
import joblib as joblib

# Carregar modelo e colunas
modelo = joblib.load("modelo_casas.pkl")
colunas = joblib.load("colunas.pkl")

# Dados novos (você só precisa fornecer os valores principais)
dados_novos = {
    "area": 100,
    "quartos": 5,
    "banheiros": 3,
    "regiao": "norte"
}


# Criar DataFrame vazio com todas as colunas do treino
nova_casa = pd.DataFrame(0, index=[0], columns=colunas)

# Preencher os valores numéricos
nova_casa["area"] = dados_novos["area"]
nova_casa["quartos"] = dados_novos["quartos"]
nova_casa["banheiros"] = dados_novos["banheiros"]

# Preencher coluna da região correta (One-Hot)
col_regiao = f"regiao_{dados_novos['regiao']}"
if col_regiao in nova_casa.columns:
    nova_casa[col_regiao] = 1

# Previsão
preco_previsto = modelo.predict(nova_casa)
print(f"Preço previsto: R$ {preco_previsto[0]:,.2f}")
