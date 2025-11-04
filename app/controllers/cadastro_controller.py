from models.usuario_model import UsuarioDB
from database import *
from auth import *
from fastapi import Request
from sqlalchemy.orm import Session


def cadastro_controller(request: Request,
                        nome:str,
                        email:str,
                        senha:str,
                        cep:str,
                        rua:str,
                        cidade:str,
                        complemento:str,
                        telefone:str,
                        db:Session):
    usuario=db.query(UsuarioDB).filter(UsuarioDB.email==email).first()
    if usuario:
        return {"mensagem":"E-mail já cadastrado"}
    senha_hash=gerar_hash_senha(senha)
    novo_usuario=UsuarioDB(nome=nome,email=email,senha=senha_hash,cep=cep,rua=rua,cidade=cidade,complemento=complemento,telefone=telefone)
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    return {"mensagem":"Usuario Cadastrado com sucesso!"}