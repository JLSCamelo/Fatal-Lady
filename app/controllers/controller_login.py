# controllers/controller_login.py
from models.usuario_model import UsuarioDB
from auth import verificar_senha, criar_token, rehash_password_if_needed
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from urllib.parse import urlencode

def login_controller(request,
                     email: str,
                     senha: str,
                     db: Session):
    """
    - Verifica usuário/senha
    - Em caso de falha: redireciona para /login?msg=invalid
    - Em caso de sucesso: seta cookie token e redireciona para /login?msg=success
    """
    usuario = db.query(UsuarioDB).filter(UsuarioDB.email == email).first()

    # Credenciais inválidas -> redireciona com msg=invalid
    if not usuario or not verificar_senha(senha, usuario.senha):
        params = urlencode({"msg": "invalid"})
        return RedirectResponse(url=f"/login?{params}", status_code=303)

    # Senha correta -> cria token
    token = criar_token({"sub": usuario.email})

    # Re-hash se necessário
    novo_hash = rehash_password_if_needed(senha, usuario.senha)
    if novo_hash:
        usuario.senha = novo_hash
        db.add(usuario)
        db.commit()

    # Redireciona com msg=success e seta cookie httponly
    params = urlencode({"msg": "success"})
    response = RedirectResponse(url=f"/login?{params}", status_code=303)
    response.set_cookie(key="token", value=token, httponly=True, max_age=60*60*24)  # opcional: ajustar max_age
    return response
