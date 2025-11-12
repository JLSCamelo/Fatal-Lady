from fastapi import APIRouter, Request, Query
from app.controllers.frete_controller import *

router = APIRouter(prefix="/api/frete", tags=["Frete"])

@router.get("/frete/calcular")
def calcular_frete(request: Request, cep_destino: str = Query(...)):
    return controller_calcular_frete(request, cep_destino)

@router.get("/frete/completar_cadastro")
def completar_cadastro(cep_destino: str = Query(...)):
    return controller_completar_cadastro(cep_destino)
