from pydantic import BaseModel, Field
from typing import List, Optional


class CasaInput(BaseModel):
    """Modelo de dados para entrada de previsão"""
    area: float = Field(..., description="Área da casa em m²", gt=0, example=100)
    quartos: int = Field(..., description="Número de quartos", ge=0, example=3)
    banheiros: int = Field(..., description="Número de banheiros", ge=0, example=2)
    regiao: str = Field(..., description="Região da casa", example="norte")

    class Config:
        json_schema_extra = {
            "example": {
                "area": 120.5,
                "quartos": 3,
                "banheiros": 2,
                "regiao": "sul"
            }
        }


class PrevisaoOutput(BaseModel):
    """Modelo de dados para saída de previsão"""
    preco_previsto: float = Field(..., description="Preço previsto em R$")
    dados_entrada: dict = Field(..., description="Dados que foram enviados")
    status: str = Field(default="success")


class ErrorResponse(BaseModel):
    """Modelo de dados para erros"""
    detail: str
    status: str = "error"


class HealthResponse(BaseModel):
    """Modelo de dados para health check"""
    status: str
    modelo_carregado: bool
    colunas_carregadas: bool
    total_colunas: int
