from app.models.usuario_model import UsuarioDB
from fastapi import Request
from datetime import datetime
from app.auth import verificar_senha, criar_token, rehash_password_if_needed
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from urllib.parse import urlencode

def login_controller(request: Request,
                     email: str,
                     senha: str,
                     db: Session):

    usuario = db.query(UsuarioDB).filter(UsuarioDB.email == email).first()

    # Se o login falhar, redireciona para /login com a mensagem de erro.
    if not usuario or not verificar_senha(senha, usuario.senha):
        return RedirectResponse(url=f"/login?msg=invalid", status_code=303)

    #criar o token no campo is_admin
    token=criar_token({"sub":usuario.email,
                       "is_admin":usuario.is_admin})
    
    #verificar se o user é admin e direcionar a rota
    if usuario.is_admin:
        destino="/admin"
    else:
        # CORREÇÃO DO REDIRECIONAMENTO DE SUCESSO:
        # (Não é mais /login?msg=success, é direto para o painel)
        destino="/me/painel"

    response = RedirectResponse(url=destino, status_code=303)
    response.set_cookie(key="token", value=token, httponly=True) 
    return response