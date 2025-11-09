from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import get_db
from auth import verificar_token
from controllers.usuario_controller import *

router = APIRouter()
templates = Jinja2Templates(directory="views/templates")

# Página inicial
@router.get("/", response_class=HTMLResponse)
def home(request: Request, db: Session = Depends(get_db)):
    return home_controller(request, db, templates)

# Painel do usuário
@router.get("/me/painel", response_class=HTMLResponse)
def painel_usuario(request: Request, db: Session = Depends(get_db)):
    return painel_controller(request, db, templates)

# Meus dados
@router.get("/me/dados", response_class=HTMLResponse)
def meus_dados(request: Request, db: Session = Depends(get_db)):
    return meus_dados_controller(request, db, templates)

# Endereços
@router.get("/me/enderecos", response_class=HTMLResponse)
def listar_endereco_usuario(request: Request, db: Session = Depends(get_db)):
    return enderecos_controller(request, db, templates)

