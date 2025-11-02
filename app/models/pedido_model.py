from sqlalchemy import Column, Integer, Float, ForeignKey, Date, String
from database import * 
from datetime import datetime
# import sql puro para add uma nova coluna
# from sqlalchemy import text
# from models.usuario_model import UsuarioDB
from sqlalchemy.orm import relationship

from sqlalchemy import Column, Integer, Float, ForeignKey, Date, String
from database import Base
from sqlalchemy.orm import relationship

#tabela Pedido
class PedidoDB(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, index=True)
    id_cliente = Column(Integer, ForeignKey("usuarios.id_cliente")) 
    data = Column(Date, default=datetime.utcnow)
    status = Column(String, default="Processo")
    valortotal = Column(Float, default=0.0)

    #relacionamento
    usuario = relationship("UsuarioDB", back_populates="pedidos")
    itens = relationship("ItemPedidoDB", back_populates="pedido")

# tabela ItemPedido
class ItemPedidoDB(Base):
    __tablename__ = "itens_pedido"

    id = Column(Integer, primary_key=True, index=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id"))  # nome da tabela corrigido
    produto_id = Column(Integer, ForeignKey("produtos.id_produto"))
    quantidade = Column(Integer)
    preco_unitario = Column(Float)

    # relações
    pedido = relationship("PedidoDB", back_populates="itens")
    produto = relationship("ProdutoDB", back_populates="itens_pedido")



#Usado para adiciona coluna sem deletar a tabela
#with engine.connect() as conexao:
#    conexao.execute(text("""
#ALTER TABLE usuarios ADD COLUMN is_admin BOOLEAN DEFAULT 0"""))
"""
db = SessionLocal()
admin=Usuario(nome="admin",email="admin@loja.com",senha=gerar_hash_senha("123456"),is_admin=True)
db.add(admin)
db.commit()
"""