from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from models.produto_model import ProdutoDB
from database import *

class UsuarioDB(Base):
    __tablename__ = "usuarios"

    id_cliente = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    senha = Column(String(255), nullable=False)
    cep = Column(String(20), nullable=True)
    rua = Column(String(255), nullable=True)
    numero = Column(String, nullable=True)
    cidade = Column(String(120), nullable=True)
    telefone = Column(String(30), nullable=True)
    is_admin = Column(Boolean, default=False)
    complemento = Column(String(120), nullable=True)

    # Relações
    pedidos = relationship("PedidoDB", back_populates="usuario")
    carrinho = relationship("CarrinhoDB", back_populates="usuario")
    enderecos = relationship("EnderecoDB", back_populates="usuario", cascade="all, delete")
