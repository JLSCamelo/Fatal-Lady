from fastapi import Request, Depends
from fastapi.responses import RedirectResponse 
from database import *
from models.produto_model import ProdutoDB
from models.usuario_model import UsuarioDB
from auth import *
from sqlalchemy.orm import Session

carrinhos = {}

def carrinho_controller(request: Request,
                        id_produto:int,
                        quantidade:int,
                        db:Session):
    token = request.cookies.get("token")
    payload=verificar_token(token)

    if not payload:
        return RedirectResponse(url="/login",status_code=303)
    
    email=payload.get("sub")
    usuario=db.query(UsuarioDB).filter_by(email=email).first()
    produto=db.query(ProdutoDB).filter_by(id=id_produto).first()

    if not produto:
        return{"mensagem":"produto não encontrado"}
    
    carrinho=carrinhos.get(usuario.id,[])
    carrinho.append({
        "id":produto.id,
        "nome":produto.nome,
        "preco":produto.preco,
        "quantidade":quantidade
    })
    carrinhos[usuario.id]=carrinho
    
    return RedirectResponse(url="/carrinho",status_code=303)