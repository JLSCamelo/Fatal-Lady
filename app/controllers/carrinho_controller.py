from fastapi import Request
from fastapi.responses import RedirectResponse 
from fastapi.templating import Jinja2Templates
from database import *
from models.produto_model import ProdutoDB
from models.usuario_model import UsuarioDB
from auth import *
from sqlalchemy.orm import Session

carrinhos = {}
templates = Jinja2Templates(directory="views/templates")

def carrinho_add(request: Request,
                        id_produto:int,
                        quantidade:int,
                        db:Session):
    token = request.cookies.get("token")
    payload=verificar_token(token)

    if not payload:
        return RedirectResponse(url="/login",status_code=303)
    
    email=payload.get("sub")
    usuario=db.query(UsuarioDB).filter_by(email=email).first()
    produto=db.query(ProdutoDB).filter_by(id_produto=id_produto).first()

    if not produto:
        return{"mensagem":"produto não encontrado"}
    
    carrinho=carrinhos.get(usuario.id_cliente,[])
    carrinho.append({
        "id":produto.id_produto,
        "nome":produto.nome,
        "preco":produto.preco,
        "quantidade":quantidade
    })
    carrinhos[usuario.id_cliente]=carrinho
    
    return RedirectResponse(url="/carrinho",status_code=303)

def carrinho_visualizar(request: Request,
                        db: Session):
    token = request.cookies.get("token")
    payload = verificar_token(token)

    if not payload:
        return RedirectResponse(url="/login",status_code=303)

    email=payload.get("sub")
    usuario=db.query(UsuarioDB).filter_by(email=email).first()
    
    carrinho=carrinhos.get(usuario.id_cliente,[])

    total=sum(item["preco"]*item["quantidade"] for item in carrinho)

    return templates.TemplateResponse("carrinho.html",
        {"request":request, "carrinho":carrinho, "total":total})