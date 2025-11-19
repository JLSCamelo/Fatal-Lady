import re
from datetime import datetime
from fastapi import APIRouter, Depends, Request, HTTPException, Form
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
from app.database import get_db
from app.controllers.excluir_conta_controller import *
from app.auth import verificar_token, verificar_senha, criar_token
from app.ultils import enviar_email
from fastapi import HTTPException
import jwt
import os
from dotenv import load_dotenv
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="app/views/templates")
router = APIRouter(prefix="/excluir", tags=["Usuários"])

load_dotenv()


@router.post("/conta") 
async def solicitar_exclusao(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("token")
    if not token:
        return RedirectResponse(url="/login", status_code=303)

    payload = verificar_token(token)
    if not payload:
        return RedirectResponse(url="/login", status_code=303)
    
    # Busca o usuário no banco
    email = payload.get("sub")
    usuario = db.query(UsuarioDB).filter_by(email=email).first()
    if not usuario:
        raise HTTPException(status_code=401, detail="Usuário não autenticado")

    token_create = criar_token({"sub": usuario.email}, expires_minutes=30)
    payload = verificar_token(token_create)
    token = payload.get("sub")
    link_confirmacao = f"{request.base_url}excluir/confirmar/{token_create}"    

    enviar_email(
        destinatario=usuario.email,
        assunto="Confirmação de Exclusão de Conta",
        corpo = f"""
<html>
  <body style="margin:0; padding:0; font-family:'Poppins',Arial,sans-serif; background-color:#fff;">
    <table width="100%" cellpadding="0" cellspacing="0">
      <!-- Cabeçalho -->
      <tr>
        <td align="center" style="padding:40px 0;">
          <img src="views/static/upload/img/catalogo/icons-main/letreiro-logo.png" width="80" alt="Fatal Lady">
          <h1 style="color:#000; font-size:28px; margin-top:10px;">FATAL <span style="color:#d00000;">LADY</span></h1>
        </td>
      </tr>

      <!-- Corpo -->
      <tr>
        <td align="center" style="padding:20px 40px;">
          <h2>Olá, {usuario.nome}! 👋</h2>
          <p style="font-size:16px; color:#333; line-height:1.6;">
            Recebemos uma solicitação para <b>excluir sua conta</b> da Fatal Lady.
          </p>
          <p style="font-size:16px; color:#333; line-height:1.6;">
            Se realmente deseja prosseguir, clique no botão abaixo.<br>
            O link é válido por <b>30 minutos</b>.
          </p>

          <a href="{link_confirmacao}"
             style="display:inline-block; margin-top:25px; background-color:#d00000; color:#fff;
                    padding:14px 28px; border-radius:6px; text-decoration:none; font-weight:bold; font-size:16px;">
            Confirmar Exclusão
          </a>

          <p style="font-size:14px; color:#666; margin-top:20px;">
            Caso não tenha solicitado esta ação, ignore este e-mail — sua conta permanecerá ativa.
          </p>
        </td>
      </tr>

      <!-- Rodapé -->
      <tr>
        <td align="center" style="padding:40px 0; background-color:#000; color:#fff; font-size:13px;">
          <p>Frete grátis em compras acima de R$299</p>
          <p>© 2025 Fatal Lady. Todos os direitos reservados.</p>
        </td>
      </tr>
    </table>
  </body>
</html>
"""

    )
    return {"message": "E-mail de confirmação enviado"}


@router.get("/confirmar/{token}", response_class=HTMLResponse)
def confirmar_exclusao_get(request: Request, token: str):
    payload = verificar_token(token)
    if not payload:
        return HTMLResponse("<h3>Link inválido ou expirado.</h3>")
    
    email = payload.get("sub")
    if not email:
        return HTMLResponse("<h3>Token sem e-mail válido.</h3>")
    
    return templates.TemplateResponse(
        "excluir_conta.html",
        {"request": request, "token": token}
    )


@router.post("/confirmar/{token}")
def confirmar_exclusao_post(
    token: str,
    cpf: str = Form(...),
    data_nascimento: str = Form(...),
    senha: str = Form(...),
    db: Session = Depends(get_db)
):
    payload = verificar_token(token)
    if not payload:
        raise HTTPException(status_code=400, detail="Link inválido ou expirado")

    email = payload.get("sub")
    if not email:
        raise HTTPException(status_code=400, detail="Token inválido")

    usuario = db.query(UsuarioDB).filter_by(email=email).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
   # Ajustar formato conforme o que vem do form
    form_data = datetime.strptime(data_nascimento, "%Y-%m-%d").date()

    # Comparar CPF e data
    if usuario.cpf != cpf or usuario.data_nascimento != form_data:
        raise HTTPException(status_code=400, detail="Dados incorretos")

    if not verificar_senha(senha, usuario.senha):
        raise HTTPException(status_code=401, detail="Senha incorreta")

    db.delete(usuario)
    db.commit()

    return {"message": "Conta excluída com sucesso"}
