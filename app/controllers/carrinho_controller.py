from fastapi import Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import datetime

from database import *
from models.produto_model import ProdutoDB
from models.usuario_model import UsuarioDB
from models.carrinho_model import CarrinhoDB, ItemCarrinhoDB
from auth import verificar_token

templates = Jinja2Templates(directory="views/templates")



def carrinho_add(request: Request, id_produto: int, quantidade: int, db: Session):
    token = request.cookies.get("token")
    payload = verificar_token(token)

    if not payload:
        return RedirectResponse(url="/login", status_code=303)

    email = payload.get("sub")
    usuario = db.query(UsuarioDB).filter_by(email=email).first()
    produto = db.query(ProdutoDB).filter_by(id_produto=id_produto).first()

    if not produto:
        return {"mensagem": "Produto não encontrado"}

    # Verifica se o carrinho do usuário já existe
    carrinho = db.query(CarrinhoDB).filter_by(id_cliente=usuario.id_cliente).first()

    if not carrinho:
        carrinho = CarrinhoDB(
            id_cliente=usuario.id_cliente,
            data=datetime.utcnow(),
            valortotal=0.0
        )
        db.add(carrinho)
        db.commit()
        db.refresh(carrinho)

    # Verifica se o produto já está no carrinho
    item = (
        db.query(ItemCarrinhoDB)
        .filter_by(carrinho_id=carrinho.id, produto_id=id_produto)
        .first()
    )

    if item:
        item.quantidade += quantidade
    else:
        item = ItemCarrinhoDB(
            carrinho_id=carrinho.id,
            produto_id=id_produto,
            quantidade=quantidade,
            preco_unitario=produto.preco
        )
        db.add(item)

        itens = db.query(ItemCarrinhoDB).filter_by(carrinho_id=carrinho.id).all()
        carrinho.valortotal = sum(item.quantidade * item.preco_unitario for item in itens)
        db.commit()

    return RedirectResponse(url="/carrinho", status_code=303)

def carrinho_remover(request: Request, produto_id: int, db: Session):
    token = request.cookies.get("token")
    payload = verificar_token(token)

    if not payload:
        return RedirectResponse(url="/login", status_code=303)

    email = payload.get("sub")
    usuario = db.query(UsuarioDB).filter_by(email=email).first()

    carrinho = db.query(CarrinhoDB).filter_by(id_cliente=usuario.id_cliente).first()

    if not carrinho:
        return RedirectResponse(url="/carrinho", status_code=303)

    item = (
        db.query(ItemCarrinhoDB)
        .filter_by(carrinho_id=carrinho.id, produto_id=produto_id)
        .first()
    )

    if item:
        db.delete(item)
        db.commit()

        itens = db.query(ItemCarrinhoDB).filter_by(carrinho_id=carrinho.id).all()
        carrinho.valortotal = sum(item.quantidade * item.preco_unitario for item in itens)
        db.commit()

    return RedirectResponse(url="/carrinho", status_code=303)

def carrinho_update(request: Request, produto_id: int, quantidade: int, db: Session):
    token = request.cookies.get("token")
    payload = verificar_token(token)

    if not payload:
        return RedirectResponse(url="/login", status_code=303)

    email = payload.get("sub")
    usuario = db.query(UsuarioDB).filter_by(email=email).first()
    carrinho = db.query(CarrinhoDB).filter_by(id_cliente=usuario.id_cliente).first()

    if not carrinho:
        return RedirectResponse(url="/carrinho", status_code=303)

    item = (
        db.query(ItemCarrinhoDB)
        .filter_by(carrinho_id=carrinho.id, produto_id=produto_id)
        .first()
    )

    if item:
        item.quantidade = quantidade
        db.commit()

        itens = db.query(ItemCarrinhoDB).filter_by(carrinho_id=carrinho.id).all()
        carrinho.valortotal = sum(item.quantidade * item.preco_unitario for item in itens)
        db.commit()

    return RedirectResponse(url="/carrinho", status_code=303)

def carrinho_visualizar(request: Request, db: Session):
    token = request.cookies.get("token")
    payload = verificar_token(token)

    if not payload:
        return RedirectResponse(url="/login", status_code=303)

    email = payload.get("sub")
    usuario = db.query(UsuarioDB).filter_by(email=email).first()
    carrinho = db.query(CarrinhoDB).filter_by(id_cliente=usuario.id_cliente).first()

    if not carrinho:
        return templates.TemplateResponse(
            "carrinho.html",
            {"request": request, "carrinho": [], "total": 0.0}
        )

    itens = db.query(ItemCarrinhoDB).filter_by(carrinho_id=carrinho.id).all()
    total = sum(item.quantidade * item.preco_unitario for item in itens)

    return templates.TemplateResponse(
        "carrinho.html",
        {"request": request, "carrinho": itens, "total": total}
    )
