from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.favorito_model import FavoritoDB
from app.models.produto_model import ProdutoDB

def listar_favoritos(id_usuario: int, db: Session):
    favoritos = db.query(FavoritoDB).filter(FavoritoDB.id_usuario == id_usuario).all()
    return [f.produto for f in favoritos]

def adicionar_favorito(id_usuario: int, id_produto: int, db: Session):
    produto = db.query(ProdutoDB).filter(ProdutoDB.id == id_produto).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    favorito_existente = db.query(FavoritoDB).filter_by(id_usuario=id_usuario, id_produto=id_produto).first()
    if favorito_existente:
        raise HTTPException(status_code=400, detail="Produto já está nos favoritos")

    favorito = FavoritoDB(id_usuario=id_usuario, id_produto=id_produto)
    db.add(favorito)
    db.commit()
    db.refresh(favorito)
    return {"message": "Produto adicionado aos favoritos com sucesso!"}

def remover_favorito(id_usuario: int, id_produto: int, db: Session):
    favorito = db.query(FavoritoDB).filter_by(id_usuario=id_usuario, id_produto=id_produto).first()
    if not favorito:
        raise HTTPException(status_code=404, detail="Favorito não encontrado")

    db.delete(favorito)
    db.commit()
    return {"message": "Produto removido dos favoritos"}
