from sqlalchemy import Column, Integer, String, Float, ForeignKey
from app.database import *
from sqlalchemy.orm import relationship

class ProdutoDB(Base):
    __tablename__ = "produtos"

    id_produto = Column(Integer,primary_key=True,index=True)
    nome = Column(String,nullable=False,index=True)
    preco = Column(Float,nullable=False)
    estoque = Column(Integer,nullable=False)
    tamanhos = Column(Integer,nullable=False)
    id_categoria = Column(Integer, ForeignKey("categoria.id"), nullable=False)
    id_fabricante = Column(Integer,nullable=False)
    caminhoimagem = Column(String,nullable=True)
    
    categoria = relationship("CategoriaDB", back_populates="produtos")
    itens_pedido = relationship("ItemPedidoDB", back_populates="produto")
    itens_carrinho = relationship("ItemCarrinhoDB",back_populates="produto",cascade="all, delete-orphan")
    favoritos = relationship("FavoritoDB", back_populates="produto", cascade="all, delete")
    itens_favoritos = relationship("ItemFavoritoDB", back_populates="produto", cascade="all, delete")


