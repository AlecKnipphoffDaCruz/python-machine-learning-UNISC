import pandas as pd
import joblib
from typing import List, Optional
from config import settings


class MLService:
    """Serviço responsável pelo modelo de Machine Learning"""



    def __init__(self):
        self.modelo = None
        self.colunas = None
        self.carregar_modelo()



    def carregar_modelo(self):
        """Carrega o modelo e as colunas"""
        try:
            self.modelo = joblib.load(settings.MODEL_PATH)
            self.colunas = joblib.load(settings.COLUMNS_PATH)
            print("✅ Modelo e colunas carregados com sucesso!")
        except FileNotFoundError as e:
            print(f"❌ Arquivo não encontrado: {e}")
            print("⚠️  Certifique-se de que modelo_casas.pkl e colunas.pkl estão no diretório")
        except Exception as e:
            print(f"❌ Erro ao carregar modelo: {e}")


    def modelo_carregado(self) -> bool:
        """Verifica se o modelo está carregado"""
        return self.modelo is not None and self.colunas is not None

   
   
    def obter_regioes(self) -> List[str]:
        """Retorna lista de regiões disponíveis"""
        if self.colunas is None:
            return []
        return [col.replace("regiao_", "") for col in self.colunas if col.startswith("regiao_")]

    
    
    def validar_regiao(self, regiao: str) -> bool:
        """Valida se a região existe"""
        col_regiao = f"regiao_{regiao.lower()}"
        return col_regiao in self.colunas

   
   
    def preparar_dados(self, area: float, quartos: int, banheiros: int, regiao: str) -> pd.DataFrame:
        """Prepara os dados para previsão"""
        # Criar DataFrame vazio com todas as colunas
        dados = pd.DataFrame(0, index=[0], columns=self.colunas)

        # Preencher valores numéricos
        dados["area"] = area
        dados["quartos"] = quartos
        dados["banheiros"] = banheiros

        # Preencher região (One-Hot Encoding)
        col_regiao = f"regiao_{regiao.lower()}"
        if col_regiao in dados.columns:
            dados[col_regiao] = 1

        return dados

  
  
    def prever(self, area: float, quartos: int, banheiros: int, regiao: str) -> float:
        """Faz a previsão do preço"""
        if not self.modelo_carregado():
            raise Exception("Modelo não carregado")

        if not self.validar_regiao(regiao):
            regioes_validas = self.obter_regioes()
            raise ValueError(f"Região '{regiao}' inválida. Regiões válidas: {regioes_validas}")

        dados = self.preparar_dados(area, quartos, banheiros, regiao)
        preco = self.modelo.predict(dados)[0]

        return float(preco)