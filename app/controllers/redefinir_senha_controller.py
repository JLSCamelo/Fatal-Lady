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
from app.auth import *

SECRET_KEY = SECRET_KEY
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
templates = Jinja2Templates(directory="app/views/templates")


load_dotenv()
EMAIL_REMITENTE = os.getenv("EMAIL_REMITENTE")
EMAIL_SENHA = os.getenv("EMAIL_SENHA")
EMAIL_FROM_NAME = os.getenv("EMAIL_FROM_NAME", EMAIL_REMITENTE)

def enviar_email(destinatario: str, nome_usuario: str, link: str):
    """
    Envia um e-mail HTML para redefinição de senha no estilo Fatal Lady.
    """
    if not EMAIL_REMITENTE or not EMAIL_SENHA:
        raise RuntimeError("Configurações de e-mail não definidas. Verifique o .env")

    msg = EmailMessage()
    msg["Subject"] = "🔒 Redefinição de senha - Fatal Lady"
    msg["From"] = EMAIL_FROM_NAME
    msg["To"] = destinatario

    html_content = f"""
    <html>
      <body style="font-family:'Poppins',Arial,sans-serif; background-color:#f9f9f9; padding:20px;">
        <table width="100%" cellpadding="0" cellspacing="0" 
               style="max-width:600px; margin:auto; background:#fff; border-radius:10px; overflow:hidden; box-shadow:0 4px 10px rgba(0,0,0,0.05);">
          
          <tr>
            <td align="center" style="padding:30px 0;">
              <h1 style="color:#000; font-size:26px; margin:0;">FATAL <span style="color:#d00000;">LADY</span></h1>
              <p style="margin-top:8px; color:#555;">Loja de calçados femininos 👠</p>
            </td>
          </tr>

          <tr>
            <td style="padding:30px;">
              <h2 style="color:#d00000;">Olá, {nome_usuario}!</h2>
              <p style="color:#333; line-height:1.6;">
                Recebemos uma solicitação para redefinir sua senha na <b>Fatal Lady</b>.
              </p>
              <p style="color:#333; line-height:1.6;">
                Se você realmente fez essa solicitação, clique no botão abaixo para criar uma nova senha:
              </p>

              <div style="text-align:center; margin:30px 0;">
                <a href="{link}" 
                   style="display:inline-block; background-color:#d00000; color:#fff; 
                          padding:14px 30px; border-radius:6px; text-decoration:none; 
                          font-weight:bold; font-size:15px;">
                  Redefinir minha senha
                </a>
              </div>

              <p style="color:#555; line-height:1.6;">
                Este link é válido por <b>1 hora</b>. Após esse período, será necessário solicitar um novo.
              </p>
              <p style="color:#555; line-height:1.6;">
                Se você não fez essa solicitação, pode ignorar este e-mail com segurança.
              </p>
            </td>
          </tr>

          <tr>
            <td align="center" style="background-color:#000; color:#fff; padding:20px; font-size:13px;">
              <p>Frete grátis em compras acima de R$299</p>
              <p>© 2025 Fatal Lady. Todos os direitos reservados.</p>
            </td>
          </tr>

        </table>
      </body>
    </html>
    """

    msg.add_alternative(html_content, subtype="html")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_REMITENTE, EMAIL_SENHA)
        smtp.send_message(msg)

def controller_esqueci_senha_login(request: Request, db: Session, email: str):
    usuario = db.query(UsuarioDB).filter_by(email=email).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    payload = {
        "sub": email,  
        "exp": datetime.utcnow() + timedelta(hours=1) 
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    link = f"http://localhost:8000/redefinir-senha?token={token}"

    enviar_email(usuario.email, usuario.nome, link)

    return RedirectResponse("/login", status_code=303)

def controller_esqueci_senha(request: Request, db: Session):
    token = request.cookies.get("token")
    if not token:
        raise HTTPException(status_code=401, detail="Usuário não autenticado")
    
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    email = payload.get("sub")

    if not email:
        raise HTTPException(status_code=400, detail="Token inválido")

    usuario = db.query(UsuarioDB).filter_by(email=email).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    # Cria o token de redefinição
    reset_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


    link = f"http://localhost:8000/redefinir-senha?token={reset_token}"

    # Envia o e-mail
    enviar_email(usuario.email, usuario.nome, link)

    return {"mensagem": "EMAIL ENVIADO"}

def controller_redefinir_senha_form(request: Request, token: str):
    return templates.TemplateResponse("redefinir_senha.html", {"request": request, "token": token})

def controller_redefinir_senha(
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
