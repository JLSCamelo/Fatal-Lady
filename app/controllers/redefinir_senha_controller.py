from fastapi import Request, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta
from email.message import EmailMessage
import smtplib
import os
from dotenv import load_dotenv
from app.models import UsuarioDB

SECRET_KEY = "seu_segredo_super_seguro"
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
templates = Jinja2Templates(directory="app/views/templates")


load_dotenv()
EMAIL_REMITENTE = os.getenv("EMAIL_REMITENTE")
EMAIL_SENHA = os.getenv("EMAIL_SENHA")
EMAIL_FROM_NAME = os.getenv("EMAIL_FROM_NAME", EMAIL_REMITENTE)
# Função utilitária
def enviar_email(destinatario: str, assunto: str, corpo: str):
    remetente = EMAIL_FROM_NAME
    senha = EMAIL_SENHA
    msg = EmailMessage()
    msg["From"] = remetente
    msg["To"] = destinatario
    msg["Subject"] = assunto
    msg.set_content(corpo)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(remetente, senha)
        smtp.send_message(msg)

def esqueci_senha(email: str, db: Session):
    usuario = db.query(UsuarioDB).filter_by(email=email).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    token = jwt.encode(
        {"sub": usuario.email, "exp": datetime.utcnow() + timedelta(hours=1)},
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    link = f"http://localhost:8000/redefinir-senha?token={token}"
    corpo = f"Olá {usuario.nome},\n\nClique no link para redefinir sua senha:\n{link}\n\nO link expira em 1 hora."

    enviar_email(usuario.email, "Redefinição de senha", corpo)
    return {"mensagem": "E-mail de recuperação enviado com sucesso!"}

def redefinir_senha_form(request: Request, token: str):
    return templates.TemplateResponse("redefinir_senha.html", {"request": request, "token": token})

def redefinir_senha(
    token: str,
    nova_senha: str,
    db: Session
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=400, detail="Token inválido ou expirado")

    usuario = db.query(UsuarioDB).filter_by(email=email).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    usuario.senha = pwd_context.hash(nova_senha)
    db.commit()

    return RedirectResponse("/login", status_code=303)
