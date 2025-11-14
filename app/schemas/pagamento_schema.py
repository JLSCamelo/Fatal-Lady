from pydantic import BaseModel, validator
from datetime import datetime
from typing import Optional, List
from enum import Enum

class StatusPagamentoStr(str, Enum):
    PENDENTE = "pendente"
    PROCESSANDO = "processando"
    APROVADO = "aprovado"
    RECUSADO = "recusado"
    CANCELADO = "cancelado"
    REEMBOLSADO = "reembolsado"

class TipoPagamentoStr(str, Enum):
    CARTAO_CREDITO = "cartao_credito"
    CARTAO_DEBITO = "cartao_debito"
    PIX = "pix"
    BOLETO = "boleto"
    TRANSFERENCIA = "transferencia"

class MetodoPagamentoStr(str, Enum):
    MERCADO_PAGO = "mercado_pago"
    PAGSEGURO = "pagseguro"
    PAGARME = "pagarme"
    STRIPE = "stripe"
    DINHEIRO = "dinheiro"

# ---------- SCHEMAS BASE ----------
class PagamentoBase(BaseModel):
    pedido_id: int
    valor_total: float
    tipo_pagamento: TipoPagamentoStr
    metodo_pagamento: MetodoPagamentoStr

class PagamentoCreate(PagamentoBase):
    @validator('valor_total')
    def valor_total_valido(cls, v):
        if v <= 0:
            raise ValueError('O valor total deve ser maior que zero')
        return v
    
    @validator('pedido_id')
    def pedido_id_valido(cls, v):
        if v <= 0:
            raise ValueError('ID do pedido inválido')
        return v

# SCHEMA PARA PAGAMENTO COM CARTÃO
class PagamentoCartaoCreate(PagamentoCreate):
    numero_cartao: str
    nome_titular: str
    data_validade: str
    cvv: str
    parcelas: int = 1
    
    @validator('numero_cartao')
    def numero_cartao_valido(cls, v):
        v = v.replace(" ", "").replace("-", "")
        if not v.isdigit() or len(v) not in [15, 16]:
            raise ValueError('Número do cartão inválido')
        return v
    
    @validator('cvv')
    def cvv_valido(cls, v):
        if not v.isdigit() or len(v) not in [3, 4]:
            raise ValueError('CVV inválido')
        return v
    
    @validator('parcelas')
    def parcelas_validas(cls, v):
        if v < 1 or v > 12:
            raise ValueError('Número de parcelas deve ser entre 1 e 12')
        return v

# SCHEMA PARA PAGAMENTO PIX
class PagamentoPixCreate(PagamentoCreate):
    chave_pix: Optional[str] = None

# SCHEMA PARA PAGAMENTO BOLETO
class PagamentoBoletoCreate(PagamentoCreate):
    pass

# SCHEMA PARA ATUALIZAÇÃO DE STATUS
class PagamentoUpdate(BaseModel):
    status: Optional[StatusPagamentoStr] = None
    id_transacao: Optional[str] = None
    mensagem_erro: Optional[str] = None
    descricao_status: Optional[str] = None
    data_aprovacao: Optional[datetime] = None
    codigo_pix: Optional[str] = None
    codigo_barras: Optional[str] = None
    url_pagamento: Optional[str] = None

# ---------- SCHEMAS DE RESPOSTA ----------
class Pagamento(PagamentoBase):
    id: int
    status: StatusPagamentoStr
    id_transacao: Optional[str] = None
    codigo_pix: Optional[str] = None
    codigo_barras: Optional[str] = None
    url_pagamento: Optional[str] = None
    ultimos_digitos_cartao: Optional[str] = None
    bandeira_cartao: Optional[str] = None
    parcelas: Optional[int] = None
    data_criacao: datetime
    data_aprovacao: Optional[datetime] = None
    data_vencimento: Optional[datetime] = None
    data_atualizacao: datetime
    mensagem_erro: Optional[str] = None
    descricao_status: Optional[str] = None

    class Config:
        from_attributes = True

# SCHEMA DETALHADO COM PEDIDO (SEM IMPORT PARA EVITAR CIRCULARIDADE)
class PagamentoDetalhado(Pagamento):
    # O pedido será serializado separadamente
    historico: List['HistoricoPagamento'] = []

    class Config:
        from_attributes = True

# SCHEMA PARA HISTÓRICO
class HistoricoPagamento(BaseModel):
    id: int
    pagamento_id: int
    status_anterior: Optional[str] = None
    status_novo: StatusPagamentoStr
    data_mudanca: datetime
    mensagem: Optional[str] = None
    id_transacao_gateway: Optional[str] = None

    class Config:
        from_attributes = True

# SCHEMAS PARA LISTAGEM
class PagamentoResumo(BaseModel):
    id: int
    pedido_id: int
    valor_total: float
    tipo_pagamento: TipoPagamentoStr
    status: StatusPagamentoStr
    data_criacao: datetime

    class Config:
        from_attributes = True

# SCHEMA SIMPLES PARA PEDIDO (EVITAR IMPORT CIRCULAR)
class PedidoResumoPagamento(BaseModel):
    id: int
    # Adicione outros campos básicos do pedido se necessário
    data_pedido: Optional[datetime] = None
    status: Optional[str] = None

    class Config:
        from_attributes = True

# SCHEMA COMPLETO COM PEDIDO
class PagamentoComPedido(Pagamento):
    pedido: Optional[PedidoResumoPagamento] = None

    class Config:
        from_attributes = True

# SCHEMA PARA WEBHOOK
class WebhookPagamento(BaseModel):
    id_transacao: str
    status: StatusPagamentoStr
    data_processamento: datetime
    mensagem: Optional[str] = None
    codigo_erro: Optional[str] = None
    valor: Optional[float] = None