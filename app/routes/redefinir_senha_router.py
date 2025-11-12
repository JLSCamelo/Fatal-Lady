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
def esqueci_senha(request: Request, db: Session = Depends(get_db)):
    return controller_esqueci_senha(request,db)

@router.post("/esqueci-senha-login")
async def esqueci_senha_login(request: Request, email: str = Form(...), db: Session = Depends(get_db)):
    return controller_esqueci_senha_login(request, db, email)

@router.get("/esqueci-senha-login", response_class=HTMLResponse)
def form_esqueci_senha(request: Request):
    return templates.TemplateResponse("esqueci_senha.html", {"request": request})

# Página de redefinição (GET)
@router.get("/redefinir-senha", response_class=HTMLResponse)
def redefinir_senha(request: Request, token: str):
    return controller_redefinir_senha_form(request, token)

# Rota para redefinir (POST)
@router.post("/redefinir-senha")
def redefinir_senha(
    token: str = Form(...),
    nova_senha: str = Form(...),
    db: Session = Depends(get_db)
):
    return controller_redefinir_senha(token, nova_senha, db)