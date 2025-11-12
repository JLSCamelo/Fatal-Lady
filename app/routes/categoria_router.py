from fastapi import APIRouter, Depends
from app.controllers.categoria_controller import *
from app.database import *
from sqlalchemy.orm import Session

router = APIRouter()

@router.get("/categorias/")
def list_categories(db:Session=Depends(get_db)):
    categorias = listar_categorias(db)
    return categorias

@router.get("/categoria/{id_categoria}/produtos")
def product_categorie(id_categoria: int, db: Session = Depends(get_db)):
    produtos = listar_produtos_categoria(db, id_categoria)
    return produtos

@router.get("/categoria/{id_categoria}/nome")
def name_categorie(id_categoria: int, db: Session = Depends(get_db)):
    nome_categoria = listar_nome_categoria(db, id_categoria)
    return nome_categoria