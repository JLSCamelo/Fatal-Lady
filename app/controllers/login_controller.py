from models.usuario_model import UsuarioDB
from fastapi import Request
from auth import verificar_senha, criar_token, rehash_password_if_needed
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from urllib.parse import urlencode

def login_controller(request: Request,
                     email: str,
                     senha: str,
                     db: Session):

    usuario = db.query(UsuarioDB).filter(UsuarioDB.email == email).first()

    # ⚡ CORREÇÃO 1: Adicionar ?msg=invalid no redirecionamento de erro
    if not usuario or not verificar_senha(senha, usuario.senha):
        # AQUI garantimos que o pop-up de senha incorreta será acionado pelo JS
        return RedirectResponse(url=f"/login?msg=invalid", status_code=303)

    # criar o token no campo is_admin
    token=criar_token({"sub":usuario.email,
                       "is_admin":usuario.is_admin})
    
    # verificar se o user é admin e direcionar a rota
    if usuario.is_admin:
        destino="/admin"
    else:
        # ⚡ CORREÇÃO 2 (Conceitual): O sucesso agora redireciona para o painel ou home (sem o ?msg=success)
        # O fato de ser redirecionado para outra página já indica sucesso.
        destino="/me/painel"

    response = RedirectResponse(url=destino, status_code=303)
    response.set_cookie(key="token", value=token, httponly=True) 
    return response
