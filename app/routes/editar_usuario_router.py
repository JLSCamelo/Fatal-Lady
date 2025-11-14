from fastapi import APIRouter, Depends, Request, Form
from sqlalchemy.orm import Session
from datetime import date
from app.database import get_db
from app.controllers.editar_usuario_controller import editar_usuario_controller
from fastapi.templating import Jinja2Templates

router = APIRouter()

templates = Jinja2Templates(directory="app/views/templates") 


#Testee
@router.get("/me/editar/dados")
def page(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse("meus_dados.html", {
        "request": request
    })

@router.post("/me/editar/dados")
def editar_usuario(
    request: Request,
    nome: str = Form(...),
    email: str = Form(...),
    telefone: str = Form(...),
    genero: str = Form(...),
    cpf: str = Form(...),
    data_nascimento: date = Form(...),
    db: Session = Depends(get_db)
):
    return editar_usuario_controller(
        request, db, nome, email, telefone, genero, cpf, data_nascimento
    )