from app.models.usuario_model import UsuarioDB
from app.database import *
from app.auth import *
from fastapi import Request, HTTPException
from sqlalchemy.orm import Session


def editar_usuario_controller(
    request: Request,
    db: Session,
    nome: str = None,
    email: str = None,
    senha: str = None,
    cep: str = None,
    rua: str = None,
    cidade: str = None,
    telefone: str = None
):

    # Verifica autenticação
    token = request.cookies.get("token")
    payload = verificar_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Usuário não autenticado")

    usuario_id = payload.get("id")
    usuario = db.query(UsuarioDB).filter(UsuarioDB.id == usuario_id).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    #  Verifica se o e-mail já está sendo usado por outro usuário
    if email:
        email_existente = db.query(UsuarioDB).filter(
            UsuarioDB.email == email, UsuarioDB.id != usuario_id
        ).first()
        if email_existente:
            raise HTTPException(status_code=400, detail="E-mail já está em uso por outro usuário")

    #  Atualiza somente os campos informados
    if nome:
        usuario.nome = nome
    if email:
        usuario.email = email
    if cep:
        usuario.cep = cep
    if rua:
        usuario.rua = rua
    if cidade:
        usuario.cidade = cidade
    if telefone:
        usuario.telefone = telefone
    if senha:
        usuario.senha = gerar_hash_senha(senha)  # Gera novo hash

    #  Salva alterações
    db.commit()
    db.refresh(usuario)

    #  Retorna resposta
    return {
        "mensagem": "Dados atualizados com sucesso!",
        "usuario": {
            "id": usuario.id,
            "nome": usuario.nome,
            "email": usuario.email,
            "cep": usuario.cep,
            "rua": usuario.rua,
            "cidade": usuario.cidade,
            "telefone": usuario.telefone
        }
    }