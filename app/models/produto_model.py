from sqlalchemy import Column, Integer, String, Float
from database import *


# from sqlalchemy.orm import relationship
# from models.produto_model import ProdutoDB

class ProdutoDB(Base):
    __tablename__ = "produtos"

    id_produto = Column(Integer, primary_key=True, index=True)
    marca = Column(String, index=True)
    tamanho = Column(Integer, null  )
    estoque = Column(Integer)
    preco = Column(Float)
    nome = Column(String, index=True)