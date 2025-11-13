from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.database import get_db
from app.controllers.editar_usuario_controller import editar_usuario_controller

router = APIRouter()

@router.put("/api/usuario/editar")
def editar_usuario(
    request: Request,
    nome: str = None,
    email: str = None,
    senha: str = None,
    cep: str = None,
    rua: str = None,
    cidade: str = None,
    telefone: str = None,
    db: Session = Depends(get_db)
):
    return editar_usuario_controller(
        request, db, nome, email, senha, cep, rua, cidade, telefone
    )