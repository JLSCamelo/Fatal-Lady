# routes/login_route.py
import json
from fastapi import APIRouter, Request, Form, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import get_db
from controllers.login_controller import login_controller

router = APIRouter()
templates = Jinja2Templates(directory="views/templates")

@router.get("/login")
def login_get(request: Request, msg: str = None):
    toast = None
    if msg == "success":
        toast = {"text": "Login feito com sucesso.", "type": "success"}
    elif msg == "invalid":
        toast = {"text": "Usuário ou senha incorretos.", "type": "error"}

    # transforma em JSON seguro para injeção direta no template
    toast_json = json.dumps(toast) if toast else "null"
    return templates.TemplateResponse("login.html", {"request": request, "toast_json": toast_json})

@router.post("/login")
def login_post(request: Request,
               email: str = Form(...),
               senha: str = Form(...),
               db: Session = Depends(get_db)):
    return login_controller(request, email, senha, db)
