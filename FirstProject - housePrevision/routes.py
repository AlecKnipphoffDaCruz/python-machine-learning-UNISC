from fastapi import APIRouter

from models import CasaInput, PrevisaoOutput, HealthResponse
from ml_service import ml_service

router = APIRouter()


@router.get("/")
def root():
    """Endpoint raiz com informações da API"""
    return {
        "message": "API de Previsão de Preços de Casas",
        "status": "online",
        "modelo_carregado": ml_service.modelo_carregado(),
        "endpoints": {
            "prever": "/prever",
            "prever_multiplas": "/prever/batch",
            "regioes_disponiveis": "/regioes",
            "health": "/health",
            "documentacao": "/docs"
        }
    }


@router.get("/regioes")
def get_regioes():
    """Retorna as regiões disponíveis para previsão"""
    if not ml_service.modelo_carregado():
        raise HTTPException(status_code=500, detail="Modelo não carregado")

    regioes = ml_service.obter_regioes()

    return {
        "regioes_disponiveis": regioes,
        "total": len(regioes)
    }


@router.post("/prever", response_model=PrevisaoOutput)
def prever_preco(casa: CasaInput):
    """Endpoint para prever o preço de uma casa"""
    if not ml_service.modelo_carregado():
        raise HTTPException(
            status_code=500,
            detail="Modelo não carregado. Verifique se os arquivos .pkl existem."
        )

    try:
        preco_previsto = ml_service.prever(
            area=casa.area,
            quartos=casa.quartos,
            banheiros=casa.banheiros,
            regiao=casa.regiao
        )

        return PrevisaoOutput(
            preco_previsto=preco_previsto,
            dados_entrada=casa.dict(),
            status="success"
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao fazer previsão: {str(e)}")


@router.post("/prever/batch")
def prever_multiplas_casas(casas: List[CasaInput]):
    """Endpoint para prever preços de múltiplas casas"""
    if not ml_service.modelo_carregado():
        raise HTTPException(status_code=500, detail="Modelo não carregado")

    resultados = []

    for i, casa in enumerate(casas):
        try:
            preco_previsto = ml_service.prever(
                area=casa.area,
                quartos=casa.quartos,
                banheiros=casa.banheiros,
                regiao=casa.regiao
            )

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
    """Verifica se a API e o modelo estão funcionando"""
    colunas_carregadas = ml_service.colunas is not None

    return HealthResponse(
        status="healthy" if ml_service.modelo_carregado() else "unhealthy",
        modelo_carregado=ml_service.modelo is not None,
        colunas_carregadas=colunas_carregadas,
        total_colunas=len(ml_service.colunas) if colunas_carregadas else 0
    )

