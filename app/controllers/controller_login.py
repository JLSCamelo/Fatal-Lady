from models.usuario_model import UsuarioDB
from database import * #tirar
from auth import *
from fastapi import Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session



#criar tabelas
Base.metadata.create_all(bind=engine) #tirar


def login_controller(request: Request,
                     email: str,
                     senha: str,
                     db: Session):
    usuario = db.query(UsuarioDB).filter(UsuarioDB.email == email).first()

    if not usuario or not verificar_senha(senha, usuario.senha):
        return {"mensagem": "Credenciais inválidas"}

    token = criar_token({"sub": usuario.email})
    response = RedirectResponse(url="/login", status_code=303)
    response.set_cookie(key="token", value=token, httponly=True)
    return response
