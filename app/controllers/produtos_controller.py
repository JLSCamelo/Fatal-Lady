from models.produto_model import ProdutoDB
from database import *
from sqlalchemy import Date
from fastapi import Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from auth import verificar_token
from models.usuario_model import UsuarioDB
from models.carrinho_model import CarrinhoDB, ItemCarrinhoDB
from models.produto_model import ProdutoDB
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="views/templates")

#criar tabelas
Base.metadata.create_all(bind=engine)


def listar_produto():
    db = SessionLocal()
    try:
        produtos = db.query(ProdutoDB).all() 
        return produtos
    except Exception as erro:
        raise erro 
    finally:
        db.close()

def produtos_por_categoria():
    db = SessionLocal()
    try:
        produtos =db.query(ProdutoDB).all() 
        # Agrupar produtos por categoria
        produtos_por_categoria = {}
        for p in produtos:
            categoria = p.categoria.strip().lower()
            if categoria not in produtos_por_categoria:
                produtos_por_categoria[categoria] = []
            produtos_por_categoria[categoria].append(p)
    except Exception as erro:
        raise erro
    finally:
        db.close()


def get_produto(request: Request, id_produto: int, db: Session):
    token = request.cookies.get("token")
    payload = verificar_token(token)

    if not payload:
        return RedirectResponse(url="/login", status_code=303)

    email = payload.get("sub")
    produto = db.query(ProdutoDB).filter(ProdutoDB.id_produto == id_produto).first()
    usuario = db.query(UsuarioDB).filter_by(email=email).first()
    return produto, usuario



# Criar produto (somente se logado)
def criar_produto(request: Request, produto: ProdutoDB, db: Session):
    try:
        # Verifica token
        token = request.cookies.get("token")
        payload = verificar_token(token)
        if not payload:
            return RedirectResponse(url="/login", status_code=303)

        email = payload.get("sub")

        db.add(produto)
        db.commit()
        db.refresh(produto)

        return produto
    except Exception as erro:
        db.rollback()
        raise erro
    finally:
        db.close()

def atualizar_produto(
    id_produto: int, data: Date, metodo: str):
    db = SessionLocal() 
    try:
        produto = db.query(ProdutoDB).filter(ProdutoDB.id == id_produto).first()
        if produto:
            produto.data = data
            produto.metodo = metodo    
            db.commit()
            db.refresh(produto)
            return produto
        return None
    except Exception as erro:
        db.rollback()
        raise erro  
    finally:
        db.close()

def deletar_produto(id_produto: int):
    db = SessionLocal()
    try:
        produto=db.query(ProdutoDB).filter(ProdutoDB.id==id_produto).first()
        if produto:
            db.delete(produto)
            db.commit()
            return True
        return False
    except Exception as erro:
        db.rollback()
        raise erro
    finally:
        db.close()

def produtos_visualizar(request: Request, db: Session):
    token = request.cookies.get("token")
    payload = verificar_token(token)

    if not payload:
        return RedirectResponse(url="/login", status_code=303)

    email = payload.get("sub")
    usuario = db.query(UsuarioDB).filter_by(email=email).first()

    produtos = listar_produto()

    return templates.TemplateResponse(
        "catalogo.html",
        {"request": request, "usuario": usuario, "produtos": produtos}
    )