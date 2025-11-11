from fastapi import Request, Form, Depends, APIRouter
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from app.controllers.redefinir_senha_controller import *
from app.database import get_db


app = APIRouter()

# Rota para solicitar redefinição
@app.post("/esqueci-senha")
def esqueci_senha(email: str = Form(...), db: Session = Depends(get_db)):
    return esqueci_senha(email,db)

# Página de redefinição (GET)
@app.get("/redefinir-senha", response_class=HTMLResponse)
def redefinir_senha_form(request: Request, token: str):
    return redefinir_senha_form(request, token)

# Rota para redefinir (POST)
@app.post("/redefinir-senha")
def redefinir_senha(
    token: str = Form(...),
    nova_senha: str = Form(...),
    db: Session = Depends(get_db)
):
    return redefinir_senha(token, nova_senha, db)