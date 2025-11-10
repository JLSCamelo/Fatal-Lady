from fastapi import Request, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.auth import verificar_token
from app.database import get_db
from app.models.usuario_model import UsuarioDB
from app.models.enderecos_model import EnderecoDB


def listar_enderecos(request: Request, db: Session):
    token = request.cookies.get("token")
    if not token:
        return RedirectResponse(url="/login", status_code=303)

    payload = verificar_token(token)
    if not payload:
        return RedirectResponse(url="/login", status_code=303)

    email = payload.get("sub")
    usuario = db.query(UsuarioDB).filter_by(email=email).first()

    if not usuario:
        return RedirectResponse(url="/login", status_code=303)

    enderecos = db.query(EnderecoDB).filter_by(id_cliente=usuario.id_cliente).all()
    return enderecos


def criar_endereco(request: Request, db: Session, cep: str, rua: str, cidade: str, complemento: str):
    token = request.cookies.get("token")
    if not token:
        return RedirectResponse(url="/login", status_code=303)

    payload = verificar_token(token)
    if not payload:
        return RedirectResponse(url="/login", status_code=303)

    email = payload.get("sub")
    usuario = db.query(UsuarioDB).filter_by(email=email).first()

    if not usuario:
        return RedirectResponse(url="/login", status_code=303)

    novo_endereco = EnderecoDB(
        id_cliente=usuario.id_cliente,
        cep=cep,
        rua=rua,
        cidade=cidade,
        complemento=complemento
    )

    db.add(novo_endereco)
    db.commit()
    db.refresh(novo_endereco)

    return novo_endereco



