from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import get_db
from controllers.cadastro_controller import *
from auth import *

router = APIRouter()
templates = Jinja2Templates(directory="views/templates")

# Página do formulário de cadastro
@router.get("/cadastrar", response_class=HTMLResponse)
def pagina_cadastro(request: Request):
    return templates.TemplateResponse(
        "registrar.html", 
        {"request": request}
    )

# Cadastro de novo usuário
@router.post("/cadastrar")
def cadastrar_usuario(
    request: Request,
    nome: str = Form(...),
    email: str = Form(...),
    senha: str = Form(...),
    cep: str = Form(...),
    rua: str = Form(...),
    cidade: str = Form(...),
    telefone: str = Form(...),
    db: Session = Depends(get_db) 
):
    resultado = cadastro_controller(
        request, nome, email, senha, cep, rua, cidade, telefone, db
    )
    return RedirectResponse(url="/login", status_code=303)
