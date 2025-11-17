from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.models.enderecos_model import EnderecoDB
from app.models.usuario_model import UsuarioDB
from app.auth import *



def listar_enderecos(request, db: Session):
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

    enderecos = db.query(EnderecoDB).filter_by(usuario_id=usuario.id_cliente).all()

    return {"usuario": usuario, "enderecos": enderecos}


def criar_endereco(request, cep, rua, bairro, cidade, estado, complemento, numero, apelido, destinatario, principal, db: Session):
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
        usuario_id=usuario.id_cliente,
        cep=cep,
        rua=rua,
        bairro=bairro,
        cidade=cidade,
        estado=estado,
        complemento=complemento,
        numero=numero,
        apelido=apelido,
        destinatario=destinatario,
        principal = True if principal else False
    )

    db.add(novo_endereco)
    db.commit()
    db.refresh(novo_endereco)

    return RedirectResponse(url="/me/enderecos", status_code=303)

