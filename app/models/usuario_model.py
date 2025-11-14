from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.produto_model import ProdutoDB
from app.database import *

class UsuarioDB(Base):
    __tablename__ = "usuarios"

    id_cliente = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    senha = Column(String(255), nullable=False)
    telefone = Column(String(30), nullable=False)
    is_admin = Column(Boolean, default=False)
    cpf = Column(String(11), nullable=False) #colcoar unique
    genero = Column(String, nullable=False)
    data_nascimento = Column(Date, nullable=False)
    ultima_atividade = Column(DateTime, default=datetime.utcnow)


    # Relações
    pedidos = relationship("PedidoDB", back_populates="usuario")
    carrinho = relationship("CarrinhoDB", back_populates="usuario")
    enderecos = relationship("EnderecoDB", back_populates="usuario", cascade="all, delete")
    favoritos = relationship("FavoritoDB", back_populates="usuario", cascade="all, delete")
