from pathlib import Path


class Settings:
    """Configurações da aplicação"""

    # Informações da API
    APP_NAME = "API de Previsão de Preços de Casas"
    APP_VERSION = "1.0.0"
    APP_DESCRIPTION = "API para prever preços de casas baseado em características"

    # Caminhos dos arquivos
    BASE_DIR = Path(__file__).parent
    MODEL_PATH = BASE_DIR / "modelo_casas.pkl"
    COLUMNS_PATH = BASE_DIR / "colunas.pkl"

    # Configurações do servidor
    HOST = "0.0.0.0"
    PORT = 8000
    DEBUG = True


settings = Settings()