from fastapi import APIRouter, HTTPException
from typing import List
from models import CasaInput, PrevisaoOutput, HealthResponse
from ml_service import ml_service

router = APIRouter()


@router.get("/")
def root():
    return {
        "message": "API de Previsão de Preços de Casas",
        "status": "online",
        "modelo_carregado": ml_service.modelo_carregado(),
        "endpoints": {
            "prever": "/prever",
            "prever_multiplas": "/prever/batch",
            "health": "/health",
            "documentacao": "/docs"
        }
    }


@router.post("/prever", response_model=PrevisaoOutput)
def prever_preco(casa: CasaInput):
    if not ml_service.modelo_carregado():
        raise HTTPException(status_code=500, detail="Modelo não carregado")

    dados = casa.dict()
    preco_previsto = ml_service.prever(dados)

    return PrevisaoOutput(
        preco_previsto=preco_previsto,
        dados_entrada=dados,
        status="success"
    )


@router.post("/prever/batch")
def prever_multiplas_casas(casas: List[CasaInput]):
    if not ml_service.modelo_carregado():
        raise HTTPException(status_code=500, detail="Modelo não carregado")

    resultados = []

    for i, casa in enumerate(casas):
        try:
            preco_previsto = ml_service.prever(casa.dict())

            resultados.append({
                "index": i,
                "preco_previsto": preco_previsto,
                "dados": casa.dict(),
                "status": "success"
            })

        except Exception as e:
            resultados.append({
                "index": i,
                "erro": str(e),
                "dados": casa.dict(),
                "status": "error"
            })

    return {
        "total_casas": len(casas),
        "previsoes": resultados
    }


@router.get("/health", response_model=HealthResponse)
def health_check():
    return HealthResponse(
        status="healthy" if ml_service.modelo_carregado() else "unhealthy",
        modelo_carregado=ml_service.modelo is not None,
        colunas_carregadas=ml_service.features is not None,
        total_colunas=len(ml_service.features) if ml_service.features else 0
    )
