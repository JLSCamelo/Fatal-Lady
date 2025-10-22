from sqlalchemy import Column, Integer, String, Float
from database import *

# from sqlalchemy.orm import relationship
# from models.produto_model import ProdutoDB

class ProdutoDB(Base):
    __tablename__ = "produtos"

    id_produto = Column(Integer,primary_key=True,index=True)
<<<<<<< HEAD
    nome = Column(String,nullable=False,index=True)
    preco = Column(Float,nullable=False)
    estoque = Column(Integer,nullable=False)
    tamanhos = Column(Integer,nullable=False)
    id_categoria = Column(String,nullable=True)
    id_fabricante = Column(Integer,nullable=False)
    caminhoimagem = Column(String,nullable=True)
    
=======
    marca = Column(String,nullable=False,index=True)
    tamanho = Column(Integer,nullable=False)
    estoque = Column(Integer,nullable=False)
    preco = Column(Float,nullable=False)
    nome = Column(String,nullable=False,index=True)
    imagem = Column(String,nullable=True)
    categoria = Column(String,nullable=False)
  
>>>>>>> 45833ccc4ef94b15890ebafc0aa288548945ec6e

#criar banco e tabelas
Base.metadata.create_all(bind=engine)

"""
marca = "Adidas"
tamanho = "G"
estoque = 500
preco = 350.00
nome = "Blusa"
imagem = "Sem Imagem"
novo=ProdutoDB(marca=marca, tamanho=tamanho, estoque=estoque, preco=preco, nome=nome, imagem=imagem)

db=SessionLocal()
db.add(novo)
db.commit()
"""