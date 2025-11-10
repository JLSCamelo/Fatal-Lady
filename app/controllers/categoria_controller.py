from fastapi import HTTPException
from app.database import *
from app.models.produto_model import ProdutoDB
from app.models.categoria_model import CategoriaDB
from sqlalchemy.orm import Session


def listar_categorias(db: Session):
    categorias = db.query(CategoriaDB).all()
    return categorias

def listar_produtos_categoria(db:Session, id_categoria:int):
    produtos = db.query(ProdutoDB).filter(ProdutoDB.id_categoria == id_categoria).all()
    if not produtos:
        raise HTTPException(status_code=404, detail="Nenhum produto encontrado para essa categoria")
    return produtos

def listar_nome_categoria(db:Session, id_categoria:int):
    categoria = db.query(CategoriaDB).filter(CategoriaDB.id == id_categoria).first()
    if not categoria:
        raise HTTPException(status_code=404, detail="Nenhuma categoria encontrado")
    return categoria.nome