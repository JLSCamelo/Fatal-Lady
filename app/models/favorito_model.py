from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

# Tabela de Favoritos
class FavoritoDB(Base):
    __tablename__ = "favoritos"

    id = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer, ForeignKey("usuarios.id_cliente", ondelete="CASCADE"))
    id_produto = Column(Integer, ForeignKey("produtos.id_produto", ondelete="CASCADE"))

    usuario = relationship("UsuarioDB", back_populates="favoritos")
    produto = relationship("ProdutoDB", back_populates="favoritos")
    itens = relationship("ItemFavoritoDB", back_populates="favorito", cascade="all, delete")



# Itens dentro dos favoritos 
class ItemFavoritoDB(Base):
    __tablename__ = "itens_favoritos"

    id = Column(Integer, primary_key=True, index=True)
    favorito_id = Column(Integer, ForeignKey("favoritos.id", ondelete="CASCADE"))
    produto_id = Column(Integer, ForeignKey("produtos.id_produto", ondelete="CASCADE"))
    preco_unitario = Column(Float)
    tamanho = Column(Integer)

    favorito = relationship("FavoritoDB", back_populates="itens")
    produto = relationship("ProdutoDB", back_populates="itens_favoritos")
