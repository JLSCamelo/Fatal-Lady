from fastapi.responses import RedirectResponse
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.enderecos_model import EnderecoDB
from app.models.usuario_model import UsuarioDB
from app.auth import verificar_token



def _usuario_autenticado(request, db: Session) -> UsuarioDB:
    token = request.cookies.get("token")
    if not token:
        raise HTTPException(status_code=401, detail="Usuário não autenticado")

    payload = verificar_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Token inválido")

    usuario_id = payload.get("id")
    if not usuario_id:
        raise HTTPException(status_code=401, detail="Token inválido: usuário sem ID")
    
    try:
        usuario_id = int(usuario_id)
    except (TypeError, ValueError):
        raise HTTPException(status_code=400, detail="Token inválido: ID do usuário inválido")

    usuario = db.query(UsuarioDB).filter_by(id_cliente=usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    return usuario


def listar_enderecos(request, db: Session):
    try:
        usuario = _usuario_autenticado(request, db)
    except HTTPException:
        return RedirectResponse(url="/login", status_code=303)
    
    enderecos = db.query(EnderecoDB).filter_by(usuario_id=usuario.id_cliente).all()

    return {"usuario": usuario, "enderecos": enderecos}


def salvar_endereco(
    request,
    cep,
    rua,
    bairro,
    cidade,
    estado,
    complemento,
    numero,
    apelido,
    destinatario,
    principal,
    db: Session,
    endereco_id: int | None = None,
):
    try:
        usuario = _usuario_autenticado(request, db)
    except HTTPException:
        return RedirectResponse(url="/login", status_code=303)

    principal_flag = True if principal else False

    if endereco_id:
        endereco = (
            db.query(EnderecoDB)
            .filter_by(id=endereco_id, usuario_id=usuario.id_cliente)
            .first()
        )
        if not endereco:
            raise HTTPException(status_code=404, detail="Endereço não encontrado")

        endereco.cep = cep
        endereco.rua = rua
        endereco.bairro = bairro
        endereco.cidade = cidade
        endereco.estado = estado
        endereco.complemento = complemento
        endereco.numero = numero
        endereco.apelido = apelido
        endereco.destinatario = destinatario
        endereco.principal = principal_flag
    else:
        endereco = EnderecoDB(
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
            principal=principal_flag,
        )
        db.add(endereco)

    if principal_flag:
        db.query(EnderecoDB).filter(
            EnderecoDB.usuario_id == usuario.id_cliente, EnderecoDB.id != endereco.id
        ).update({EnderecoDB.principal: False})

    db.commit()
    db.refresh(endereco)

    return RedirectResponse(url="/me/enderecos", status_code=303)


def definir_endereco_principal(request, endereco_id: int, db: Session):
    usuario = _usuario_autenticado(request, db)

    endereco = (
        db.query(EnderecoDB)
        .filter_by(id=endereco_id, usuario_id=usuario.id_cliente)
        .first()
    )
    if not endereco:
        raise HTTPException(status_code=404, detail="Endereço não encontrado")

    db.query(EnderecoDB).filter(EnderecoDB.usuario_id == usuario.id_cliente).update(
        {EnderecoDB.principal: False}
    )
    endereco.principal = True
    db.commit()

    return {"mensagem": "Endereço principal atualizado"}


def remover_endereco(request, endereco_id: int, db: Session):
    usuario = _usuario_autenticado(request, db)

    endereco = (
        db.query(EnderecoDB)
        .filter_by(id=endereco_id, usuario_id=usuario.id_cliente)
        .first()
    )
    if not endereco:
        raise HTTPException(status_code=404, detail="Endereço não encontrado")

    db.delete(endereco)
    db.commit()

    return {"mensagem": "Endereço removido com sucesso"}

