import joblib
import pandas as pd
from typing import List
from config import settings

class MLService:
    def __init__(self):
        self.modelo = None
        self.features = None
        self.carregar_modelo()

    def carregar_modelo(self):
        try:
            self.modelo = joblib.load(settings.MODEL_PATH)   
            self.features = joblib.load(settings.COLUMNS_PATH)
            print("Modelo e features carregados.")
        except Exception as e:
            print("Erro ao carregar modelo:", e)
            self.modelo = None
            self.features = None

    def modelo_carregado(self) -> bool:
        return self.modelo is not None and self.features is not None

    def _prepare_input_df(self, data: dict) -> pd.DataFrame:
        if self.features is None:
            raise Exception("Features não carregadas")

        df = pd.DataFrame([{f: data.get(f, None) for f in self.features}])

        bool_map = {"sim": 1, "nao": 0, "não": 0}

        for b in [
            "mobiliado","elevador","churrasqueira","piscina","area_servico",
            "armarios_embutidos","seguranca_24h","playground","academia",
            "salao_festas","sacada_varanda","quintal","pet_friendly"
        ]:
            if b in df.columns:
                val = df.loc[0, b]
                if isinstance(val, str):
                    df.loc[0, b] = bool_map.get(val.lower(), val)

        return df

    def prever(self, input_data: dict) -> float:
        if not self.modelo_carregado():
            raise Exception("Modelo não carregado")

        df = self._prepare_input_df(input_data)
        return float(self.modelo.predict(df)[0])

    def obter_campos_necessarios(self) -> List[str]:
        return self.features or []


ml_service = MLService()
