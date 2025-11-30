import pandas as pd
import joblib

modelo = joblib.load("models/best_model.pkl")
features = joblib.load("models/columns.pkl")

dados = {
    "tipo_imovel": "casa",
    "area_m2": 120,
    "quartos": 3,
    "suites": 1,
    "banheiros": 2,
    "vagas_garagem": 2,
    "bairro": "Centro",
    "pet_friendly": "sim",
    "mobiliado": "nao",
    "condominio_valor": 350,
    "iptu_mensal": 90,
    "proximidade_centro": "perto",
    "andar": None,
    "elevador": "nao",
    "area_privativa_m2": 110,
    "churrasqueira": "sim",
    "piscina": "nao",
    "area_servico": "sim",
    "armarios_embutidos": "sim",
    "seguranca_24h": "nao",
    "playground": "nao",
    "academia": "nao",
    "salao_festas": "nao",
    "sacada_varanda": "sim",
    "quintal": "sim",
    "estado_conservacao": "novo",
    "orientacao_solar": "norte",
}

df = pd.DataFrame([dados], columns=features)

preco = modelo.predict(df)[0]

print(f"Preço previsto: R$ {preco:,.2f}")
