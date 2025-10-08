from models.produto_model import ProdutoDB
from database import *
from sqlalchemy import Date

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

def get_produto(id_produto):
    db = SessionLocal()
    try:
        produto = db.query(ProdutoDB).filter(ProdutoDB.id_produto==id_produto).first()
        return produto
    except Exception as erro:
        raise erro
    finally:
        db.close()
    



#Terminar
def criar_produto(produto: ProdutoDB):
    db = SessionLocal()
    try:
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
