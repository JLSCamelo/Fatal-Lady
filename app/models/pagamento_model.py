from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime


class PagamentoDB(Base):
    __tablename__ = "pagamentos"

    id = Column(Integer, primary_key=True, index=True)

    # RELAÇÃO COM PEDIDO (OBRIGATÓRIA)
    pedido_id = Column(Integer, ForeignKey("pedidos.id"), nullable=False, index=True)

    # INFORMAÇÕES DE PAGAMENTO
    valor_total = Column(Float, nullable=False)
    tipo_pagamento = Column(String(50), nullable=False)       # Ex: "cartao_credito"
    metodo_pagamento = Column(String(50), nullable=False)     # Ex: "mercado_pago"
    status = Column(String(50), default="pendente", index=True)

    # DADOS TRANSACIONAIS
    id_transacao = Column(String(100), nullable=True, unique=True, index=True)
    codigo_pix = Column(Text, nullable=True)
    codigo_barras = Column(String(100), nullable=True)


    # INFORMAÇÕES DE CARTÃO
    ultimos_digitos_cartao = Column(String(4), nullable=True)
    bandeira_cartao = Column(String(20), nullable=True)
    parcelas = Column(Integer, default=1)

    # DATAS IMPORTANTES
    data_criacao = Column(DateTime, default=datetime.utcnow)
    data_aprovacao = Column(DateTime, nullable=True)
    data_vencimento = Column(DateTime, nullable=True)
    data_atualizacao = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # RELACIONAMENTO
    pedido = relationship("PedidoDB", back_populates="pagamentos")


