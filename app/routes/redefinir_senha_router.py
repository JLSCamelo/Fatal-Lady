from fastapi import Request, Form, Depends, APIRouter
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from app.controllers.redefinir_senha_controller import *
from fastapi.templating import Jinja2Templates
from app.database import get_db


router = APIRouter()
templates = Jinja2Templates(directory="app/views/templates")

# Rota para solicitar redefinição
@router.post("/esqueci-senha")
def esqueci_senha(email: str = Form(...), db: Session = Depends(get_db)):
    return esqueci_senha(email,db)

# Página de redefinição (GET)
@router.get("/redefinir-senha", response_class=HTMLResponse)
def redefinir_senha_form(request: Request, token: str):
    return redefinir_senha_form(request, token)

# Rota para redefinir (POST)
@router.post("/redefinir-senha")
def redefinir_senha(
    token: str = Form(...),
    nova_senha: str = Form(...),
    db: Session = Depends(get_db)
):
    return redefinir_senha(token, nova_senha, db)