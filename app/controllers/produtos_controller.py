from app.database import *
from sqlalchemy import Date
from fastapi import Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.auth import verificar_token
from app.models.usuario_model import UsuarioDB
from app.models.produto_model import ProdutoDB
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="app/views/templates")

def listar_produto(request: Request, db: Session):
    token = request.cookies.get("token")

    if token:
        payload = verificar_token(token)

        if payload: 
            email = payload.get("sub")
            usuario = db.query(UsuarioDB).filter_by(email=email).first()
        else:
            usuario = None  # token inválido
    else:
        usuario = None  # nenhum token no cookie

    produtos = db.query(ProdutoDB).all()

    return templates.TemplateResponse(
        "catalogo.html",
        {"request": request, "usuario": usuario, "produtos": produtos}
    )


def produtos_por_categoria():
    db = SessionLocal()
    try:
        produtos =db.query(ProdutoDB).all() 
        produtos_por_categoria = {}
        if not produtos:
            return {}

        for p in produtos:
            categoria = p.categoria.strip().lower()
            if categoria not in produtos_por_categoria:
                produtos_por_categoria[categoria] = []
            produtos_por_categoria[categoria].append(p)
        return produtos_por_categoria
    except Exception as erro:
        raise erro
    finally:
        db.close()


def get_produto(request: Request, id_produto: int, db: Session):
    token = request.cookies.get("token")
    if not token:
        return RedirectResponse(url="/login", status_code=303)

    payload = verificar_token(token)

    if not payload:
        return RedirectResponse(url="/login", status_code=303)

    email = payload.get("sub")
    produto = db.query(ProdutoDB).filter(ProdutoDB.id_produto == id_produto).first()
    usuario = db.query(UsuarioDB).filter_by(email=email).first()
    return templates.TemplateResponse("produto.html", {
        "request": request,
        "produto": produto,
        "usuario": usuario
    })
