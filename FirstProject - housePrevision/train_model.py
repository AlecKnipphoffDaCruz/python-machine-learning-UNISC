import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np
import joblib

# 1. Carregar o CSV
df = pd.read_csv("data/houses.csv") 

# 2. Ver primeiras linhas
print(df.head())

# 3. Ver informações gerais
print(df.info())

# 4. Estatísticas descritivas
print(df.describe())

# 5. Ver valores únicos da coluna regiao
print(df["regiao"].unique())

df_encoded = pd.get_dummies(df, columns=["regiao"])

# Escolhendo o Target
X = df_encoded.drop("preco", axis=1)
y = df_encoded["preco"]               #Target

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print("Formato X_train :", X_train.shape)
print("Formato X_test :", X_test.shape)


modelo = LinearRegression()
modelo.fit(X_train, y_train)


y_pred = modelo.predict(X_test)

mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print ("mae: ", mae)
print ("rmse: ", rmse)
print ("r2: ", r2)


joblib.dump(modelo, "modelo_casas.pkl")
joblib.dump(X_train.columns, "colunas.pkl")