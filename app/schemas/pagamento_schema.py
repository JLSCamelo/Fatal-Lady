from pydantic import BaseModel
from datetime import datetime
from typing import Optional


# ======== BASE ========
class PagamentoBase(BaseModel):
    valor_total: float
    tipo_pagamento: str
    metodo_pagamento: str
    status: Optional[str] = "pendente"

    id_transacao: Optional[str] = None
    codigo_pix: Optional[str] = None
    codigo_barras: Optional[str] = None

    ultimos_digitos_cartao: Optional[str] = None
    bandeira_cartao: Optional[str] = None
    parcelas: Optional[int] = 1


# ======== CREATE ========
class PagamentoCreate(PagamentoBase):
    pedido_id: int


# ======== UPDATE ========
class PagamentoUpdate(BaseModel):
    valor_total: Optional[float] = None
    tipo_pagamento: Optional[str] = None
    metodo_pagamento: Optional[str] = None
    status: Optional[str] = None

    id_transacao: Optional[str] = None
    codigo_pix: Optional[str] = None
    codigo_barras: Optional[str] = None

    ultimos_digitos_cartao: Optional[str] = None
    bandeira_cartao: Optional[str] = None
    parcelas: Optional[int] = None

    data_aprovacao: Optional[datetime] = None
    data_vencimento: Optional[datetime] = None


# ======== RESPONSE ========
class PagamentoResponse(PagamentoBase):
    id: int
    pedido_id: int

    data_criacao: datetime
    data_aprovacao: Optional[datetime]
    data_vencimento: Optional[datetime]
    data_atualizacao: datetime

    class Config:
        from_attributes = True
