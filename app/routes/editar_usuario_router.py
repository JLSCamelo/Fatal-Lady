from fastapi import APIRouter, Depends, Request, Form
from sqlalchemy.orm import Session
from datetime import date
from app.database import get_db
from app.controllers.editar_usuario_controller import editar_usuario_controller
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/me")

templates = Jinja2Templates(directory="app/views/templates") 


@router.post("/editar/dados")
def editar_usuario(
    request: Request,
    nome: str = Form(None),
    email: str = Form(None),
    telefone: str = Form(None),
    genero: str = Form(None),
    cpf: str = Form(None),
    data_nascimento: date = Form(None),
    db: Session = Depends(get_db)
):
    return editar_usuario_controller(
        request, db, nome, email, telefone, genero, cpf, data_nascimento
    )