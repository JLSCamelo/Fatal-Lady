from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime
import enum

# STATUS E TIPOS DE PAGAMENTO
class StatusPagamento(enum.Enum):
    PENDENTE = "pendente"
    PROCESSANDO = "processando"
    APROVADO = "aprovado"
    RECUSADO = "recusado"
    CANCELADO = "cancelado"
    REEMBOLSADO = "reembolsado"

class TipoPagamento(enum.Enum):
    CARTAO_CREDITO = "cartao_credito"
    CARTAO_DEBITO = "cartao_debito"
    PIX = "pix"
    BOLETO = "boleto"
    TRANSFERENCIA = "transferencia"

class MetodoPagamento(enum.Enum):
    MERCADO_PAGO = "mercado_pago"
    PAGSEGURO = "pagseguro"
    PAGARME = "pagarme"
    STRIPE = "stripe"
    DINHEIRO = "dinheiro"

class PagamentoDB(Base):
    __tablename__ = "pagamentos"

    id = Column(Integer, primary_key=True, index=True)
    
    # RELAÇÃO COM PEDIDO (OBRIGATÓRIA) 
    pedido_id = Column(Integer, ForeignKey("pedidos.id"), nullable=False, index=True)

    # INFORMAÇÕES DE PAGAMENTO
    valor_total = Column(Float, nullable=False)
    tipo_pagamento = Column(Enum(TipoPagamento), nullable=False)
    metodo_pagamento = Column(Enum(MetodoPagamento), nullable=False)
    status = Column(Enum(StatusPagamento), default=StatusPagamento.PENDENTE, index=True)
    
    # DADOS TRANSACIONAIS
    id_transacao = Column(String(100), nullable=True, unique=True, index=True)  # ID do gateway
    codigo_pix = Column(Text, nullable=True)  # pagamentos PIX
    codigo_barras = Column(String(100), nullable=True)  # boletos
    
    # INFORMAÇÕES DE CARTÃO (criptografadas na prática)
    ultimos_digitos_cartao = Column(String(4), nullable=True)
    bandeira_cartao = Column(String(20), nullable=True)
    parcelas = Column(Integer, default=1)  # N de parcelas
    
    # DATAS IMPORTANTES
    data_criacao = Column(DateTime, default=datetime.utcnow)
    data_aprovacao = Column(DateTime, nullable=True)
    data_vencimento = Column(DateTime, nullable=True)  # boletos
    data_atualizacao = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # RELACIONAMENTO
    pedido = relationship("PedidoDB", back_populates="pagamentos")
