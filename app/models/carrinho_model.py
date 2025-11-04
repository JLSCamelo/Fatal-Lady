from sqlalchemy import Column, Integer, Float, ForeignKey, Date
from database import * 
from datetime import datetime
# import sql puro para add uma nova coluna
# from sqlalchemy import text
# from models.usuario_model import UsuarioDB
from sqlalchemy.orm import relationship
#tabela Pedido
class CarrinhoDB(Base):
    __tablename__ = "carrinho"

    id = Column(Integer, primary_key=True, index=True)
    id_cliente = Column(Integer, ForeignKey("usuarios.id_cliente")) 
    data = Column(Date, default=datetime.utcnow)
    valortotal = Column(Float, default=0.0)

    #relacionamento
    usuario = relationship("UsuarioDB", back_populates="carrinho")
    itens = relationship("ItemCarrinhoDB", back_populates="carrinho")

# tabela ItemPedido
class ItemCarrinhoDB(Base):
    __tablename__ = "itens_carrinho"

    id = Column(Integer, primary_key=True, index=True)
    carrinho_id = Column(Integer, ForeignKey("carrinho.id"))
    produto_id = Column(Integer, ForeignKey("produtos.id_produto"))
    quantidade = Column(Integer)
    preco_unitario = Column(Float)
    tamanho = Column(Integer)

    # relações
    carrinho = relationship("CarrinhoDB", back_populates="itens")
    produto = relationship("ProdutoDB", back_populates="itens_carrinho")


#criar banco e tabelas
# Base.metadata.create_all(bind=engine)

"""
db = SessionLocal()
admin=Usuario(nome="admin",email="admin@loja.com",senha=gerar_hash_senha("123456"),is_admin=True)
db.add(admin)
db.commit()
"""