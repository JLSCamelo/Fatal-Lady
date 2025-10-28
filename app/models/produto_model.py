from sqlalchemy import Column, Integer, String, Float
from database import *
from sqlalchemy.orm import relationship
# from models.produto_model import ProdutoDB

class ProdutoDB(Base):
    __tablename__ = "produtos"

    id_produto = Column(Integer,primary_key=True,index=True)
    nome = Column(String,nullable=False,index=True)
    preco = Column(Float,nullable=False)
    estoque = Column(Integer,nullable=False)
    id_categoria = Column(String,nullable=True)
    id_fabricante = Column(Integer,nullable=False)
    tamanhos = Column(Integer,nullable=False)
    caminhoimagem = Column(String,nullable=True)
    nome_categoria = Column(String,nullable=True)
    
    itens_pedido = relationship("ItemPedidoDB", back_populates="produto")

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