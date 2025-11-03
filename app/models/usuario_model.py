from sqlalchemy import Column, Integer, String, Boolean
from database import *
# from sqlalchemy import text
from sqlalchemy.orm import relationship
from models.produto_model import ProdutoDB

class UsuarioDB(Base):
    __tablename__ = "usuarios"

    id_cliente = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    senha = Column(String(255), nullable=False)
    cep = Column(String(20), nullable=True)     
    rua = Column(String(255), nullable=True)
    cidade = Column(String(120), nullable=True)
    telefone = Column(String(30), nullable=True)     
    is_admin = Column(Boolean, default=False)
    complemento = Column(String(120), nullable=True)
    #relação de tabela
    pedidos=relationship("PedidoDB",back_populates="usuario")
    carrinho =relationship("CarrinhoDB",back_populates="usuario")

    