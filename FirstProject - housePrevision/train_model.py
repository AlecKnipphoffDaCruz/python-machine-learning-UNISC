# train_model.py
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
import os

# ===============================================
# CONFIGURAÇÕES
# ===============================================
CSV_PATH = "data/houses.csv"
MODEL_DIR = "models"
MODEL_PATH = os.path.join(MODEL_DIR, "best_model.pkl")
COLUMNS_PATH = os.path.join(MODEL_DIR, "columns.pkl")
RESULTS_PATH = os.path.join(MODEL_DIR, "training_report.txt")
TARGET = "preco_venda"

os.makedirs(MODEL_DIR, exist_ok=True)

# ===============================================
# 1. CARREGAR CSV
# ===============================================
df = pd.read_csv(CSV_PATH, sep=";", encoding="utf-8")
print("Loaded:", df.shape)

# ===============================================
# 2. LIMPEZA E NORMALIZAÇÃO
# ===============================================
df.columns = [c.strip().lower() for c in df.columns]

# Substituir tokens de NA
df.replace({
    "NA": np.nan, "na": np.nan,
    "nao informado": np.nan, "": np.nan
}, inplace=True)

# Booleanos que queremos transformar
binary_cols = [
    "mobiliado", "elevador", "churrasqueira", "piscina", "area_servico",
    "armarios_embutidos", "seguranca_24h", "playground", "academia",
    "salao_festas", "sacada_varanda", "quintal", "pet_friendly"
]

binary_map = {"sim": 1, "não": 0, "nao": 0}

for col in binary_cols:
    if col in df.columns:
        df[col] = df[col].str.lower().map(binary_map)

# Numéricos que devem ser convertidos
numeric_cols = [
    "area_m2", "quartos", "suites", "banheiros", "vagas_garagem",
    "condominio_valor", "iptu_mensal", "ano_construcao", "area_privativa_m2"
]

for col in numeric_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# Remover linhas com target ausente
df[TARGET] = pd.to_numeric(df[TARGET], errors="coerce")
df = df[df[TARGET].notna()]

# ===============================================
# 3. FEATURES USADAS
# ===============================================
features = [
    "tipo_imovel", "area_m2", "quartos", "suites", "banheiros",
    "vagas_garagem", "bairro", "pet_friendly", "mobiliado",
    "condominio_valor", "iptu_mensal", "proximidade_centro",
    "andar", "elevador", "area_privativa_m2", "churrasqueira",
    "piscina", "area_servico", "armarios_embutidos", "seguranca_24h",
    "playground", "academia", "salao_festas", "sacada_varanda",
    "quintal", "estado_conservacao", "orientacao_solar"
]

features = [f for f in features if f in df.columns]

X = df[features].copy()
y = df[TARGET].copy()

# ===============================================
# 4. SPLIT
# ===============================================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ===============================================
# 5. PIPELINES DE PRÉ-PROCESSAMENTO
# ===============================================
num_features = [c for c in features if c in numeric_cols]
cat_features = [c for c in features if c not in numeric_cols]

numeric_transformer = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler())
])

categorical_transformer = Pipeline([
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("onehot", OneHotEncoder(handle_unknown="ignore"))
])

preprocessor = ColumnTransformer([
    ("num", numeric_transformer, num_features),
    ("cat", categorical_transformer, cat_features)
])

# ===============================================
# 6. MODELOS
# ===============================================
models = [
    ("LinearRegression", LinearRegression()),
    ("RandomForest", RandomForestRegressor(
        n_estimators=300,
        random_state=42,
        n_jobs=-1
    ))
]

results = []

# ===============================================
# 7. TREINAR E AVALIAR
# ===============================================
for name, model in models:
    print(f"\nTraining: {name}")

    pipe = Pipeline([
        ("pre", preprocessor),
        ("model", model)
    ])

    pipe.fit(X_train, y_train)

    preds = pipe.predict(X_test)

    mae = mean_absolute_error(y_test, preds)
    rmse = (mean_squared_error(y_test, preds)) ** 0.5
    r2 = r2_score(y_test, preds)

    print(f"{name} | MAE={mae:.2f} | RMSE={rmse:.2f} | R2={r2:.4f}")

    results.append((name, pipe, rmse))


# ===============================================
# 8. SALVAR MELHOR MODELO
# ===============================================
best_name, best_model, best_rmse = sorted(results, key=lambda x: x[2])[0]

joblib.dump(best_model, MODEL_PATH)
joblib.dump(features, COLUMNS_PATH)

with open(RESULTS_PATH, "w", encoding="utf-8") as f:
    f.write(f"Best model: {best_name}\n")
    f.write(f"RMSE: {best_rmse}\n")
    f.write(f"Used features: {features}\n")

print("\n===================================")
print("TREINAMENTO FINALIZADO COM SUCESSO!")
print("Melhor modelo:", best_name)
print("Salvo em:", MODEL_PATH)
print("Colunas salvas em:", COLUMNS_PATH)
print("===================================")
# ===============================================