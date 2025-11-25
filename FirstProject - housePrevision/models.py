# models.py
from pydantic import BaseModel, Field
from typing import Optional

class CasaInput(BaseModel):
    tipo_imovel: Optional[str] = Field(None, example="casa")
    area_m2: Optional[float] = Field(None, example=120)
    quartos: Optional[int] = Field(None, example=3)
    suites: Optional[int] = Field(None, example=1)
    banheiros: Optional[int] = Field(None, example=2)
    vagas_garagem: Optional[int] = Field(None, example=1)
    bairro: Optional[str] = Field(None, example="Centro")
    pet_friendly: Optional[str] = Field(None, example="sim")
    ano_construcao: Optional[int] = None
    mobiliado: Optional[str] = Field(None, example="nao")
    condominio_valor: Optional[float] = None
    iptu_mensal: Optional[float] = None
    proximidade_centro: Optional[str] = None
    andar: Optional[str] = None
    elevador: Optional[str] = None
    area_privativa_m2: Optional[float] = None
    churrasqueira: Optional[str] = None
    piscina: Optional[str] = None
    area_servico: Optional[str] = None
    armarios_embutidos: Optional[str] = None
    seguranca_24h: Optional[str] = None
    playground: Optional[str] = None
    academia: Optional[str] = None
    salao_festas: Optional[str] = None
    sacada_varanda: Optional[str] = None
    quintal: Optional[str] = None
    estado_conservacao: Optional[str] = None
    orientacao_solar: Optional[str] = None
    
class PrevisaoOutput(BaseModel):
    preco_previsto: float
    dados_entrada: dict
    status: str = "success"


class HealthResponse(BaseModel):
    status: str
    modelo_carregado: bool
    colunas_carregadas: bool
    total_colunas: int
