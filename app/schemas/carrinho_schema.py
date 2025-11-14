from pydantic import BaseModel, validator
from datetime import date
from typing import List, Optional
from decimal import Decimal

# ---------- ITEM CARRINHO ----------
class ItemCarrinhoBase(BaseModel):
    produto_id: int
    quantidade: int
    preco_unitario: float
    tamanho: int

class ItemCarrinhoCreate(ItemCarrinhoBase):
    @validator('quantidade')
    def quantidade_valida(cls, v):
        if v <= 0:
            raise ValueError('A quantidade deve ser maior que zero')
        return v
    
    @validator('preco_unitario')
    def preco_valido(cls, v):
        if v <= 0:
            raise ValueError('O preço deve ser maior que zero')
        return v

class ItemCarrinhoUpdate(BaseModel):
    quantidade: Optional[int] = None

class ItemCarrinho(ItemCarrinhoBase):
    id: int
    carrinho_id: int

    class Config:
        from_attributes = True

# ---------- CARRINHO ----------
class CarrinhoBase(BaseModel):
    id_cliente: int

class CarrinhoCreate(CarrinhoBase):
    pass

class Carrinho(CarrinhoBase):
    id: int
    data: date
    valortotal: float

    class Config:
        from_attributes = True

class CarrinhoComItens(Carrinho):
    itens: List[ItemCarrinho] = []

    class Config:
        from_attributes = True