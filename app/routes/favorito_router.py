from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.database import get_db
from app.controllers.favorito_controller import *
from app.auth import verificar_token 

router = APIRouter()

@router.get("/favorito")
def listar_favoritos(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("token")
    payload = verificar_token(token)
    id_usuario = payload.get("id")

    return listar_favoritos(id_usuario, db)

@router.post("/favorito/adicionar/{id_produto}")
def adicionar_favorito(id_produto: int, request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("token")
    payload = verificar_token(token)
    id_usuario = payload.get("id")

    return adicionar_favorito(id_usuario, id_produto, db)

@router.delete("/favorito/deletar/{id_produto}")
def remover_favorito(id_produto: int, request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("token")
    payload = verificar_token(token)
    id_usuario = payload.get("id")

    return remover_favorito(id_usuario, id_produto, db)
