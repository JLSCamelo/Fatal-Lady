from sqlalchemy import Column, Integer, String, Boolean, Date
from sqlalchemy.orm import relationship
from app.models.produto_model import ProdutoDB
from app.database import *

class UsuarioDB(Base):
    __tablename__ = "usuarios"

    id_cliente = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    senha = Column(String(255), nullable=False)
    cep = Column(String(20), nullable=False)
    rua = Column(String(255), nullable=False)
    numero = Column(String, nullable=False)
    cidade = Column(String(120), nullable=False)
    telefone = Column(String(30), nullable=False)
    is_admin = Column(Boolean, default=False)
    complemento = Column(String(120), nullable=True)
    cpf = Column(String(11), nullable=False)
    genero = Column(String, nullable=False)
    data_nascimento = Column(Date, nullable=False)
    estado = Column(String, nullable=False)
    bairro= Column(String, nullable=False)


    # Relações
    pedidos = relationship("PedidoDB", back_populates="usuario")
    carrinho = relationship("CarrinhoDB", back_populates="usuario")
    enderecos = relationship("EnderecoDB", back_populates="usuario", cascade="all, delete")
    favoritos = relationship("FavoritoDB", back_populates="usuario", cascade="all, delete")
