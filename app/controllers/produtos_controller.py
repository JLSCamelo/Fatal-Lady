from app.database import *
from sqlalchemy import Date
from fastapi import Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session, joinedload
from app.auth import verificar_token
from app.models.usuario_model import UsuarioDB
from app.models.produto_model import ProdutoDB
from app.models.categoria_model import CategoriaDB
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


def produtos_por_categoria(request: Request, db: Session):
    token = request.cookies.get("token")
    usuario = None

    if token:
        payload = verificar_token(token)
        if payload:
            email = payload.get("sub")
            usuario = db.query(UsuarioDB).filter_by(email=email).first()

    produtos = (
        db.query(ProdutoDB)
        .options(joinedload(ProdutoDB.categoria))
        .all()
    )

    categorias_map: dict[int, CategoriaDB] = {}
    for produto in produtos:
        if produto.categoria:
            categorias_map[produto.categoria.id] = produto.categoria

    categorias = list(categorias_map.values())

    return templates.TemplateResponse(
        "catalogo.html",
        {
            "request": request,
            "usuario": usuario,
            "produtos": produtos,
            "categorias": categorias,
        },
    )

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
