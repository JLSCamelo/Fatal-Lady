from models.usuario_model import UsuarioDB
from auth import verificar_senha, criar_token, rehash_password_if_needed
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from urllib.parse import urlencode

def login_controller(request,
                     email: str,
                     senha: str,
                     db: Session):

    usuario = db.query(UsuarioDB).filter(UsuarioDB.email == email).first()

    if not usuario or not verificar_senha(senha, usuario.senha):
        params = urlencode({"msg": "invalid"})
        return RedirectResponse(url=f"/login?{params}", status_code=303)

    token = criar_token({"sub": usuario.email})
 
    novo_hash = rehash_password_if_needed(senha, usuario.senha)
    if novo_hash:
        usuario.senha = novo_hash
        db.add(usuario)
        db.commit()

    params = urlencode({"msg": "success"})
    response = RedirectResponse(url=f"/login?{params}", status_code=303)
    response.set_cookie(key="token", value=token, httponly=True) 
    return response
