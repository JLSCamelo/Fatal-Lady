from pydantic import BaseModel, validator
from typing import Optional, List

# ---------- SCHEMAS BASE ----------
class ProdutoBase(BaseModel):
    nome: str
    descricao: Optional[str] = None
    preco: float
    estoque: int
    tamanhos: int  
    id_categoria: int
    id_fabricante: int
    caminhoimagem: Optional[str] = None

class ProdutoCreate(ProdutoBase):
    @validator('preco')
    def preco_maior_que_zero(cls, v):
        if v <= 0:
            raise ValueError('O preço deve ser maior que zero')
        return v
    
    @validator('estoque')
    def estoque_nao_negativo(cls, v):
        if v < 0:
            raise ValueError('O estoque não pode ser negativo')
        return v
    
    @validator('tamanhos')
    def tamanho_valido(cls, v):
        if v <= 0:
            raise ValueError('O tamanho deve ser maior que zero')
        return v

class ProdutoUpdate(BaseModel):
    nome: Optional[str] = None
    descricao: Optional[str] = None
    preco: Optional[float] = None
    estoque: Optional[int] = None
    tamanhos: Optional[int] = None  
    id_categoria: Optional[int] = None
    id_fabricante: Optional[int] = None
    caminhoimagem: Optional[str] = None
    ativo: Optional[int] = None

# ---------- SCHEMAS DE RESPOSTA ----------
class Produto(ProdutoBase):
    id_produto: int
    ativo: int

    class Config:
        from_attributes = True

class ProdutoComCategoria(Produto):
    from app.schemas.categoria_schema import Categoria
    categoria: Optional[Categoria] = None

class ProdutoDetalhado(ProdutoComCategoria):
    from app.schemas.fabricante_schema import Fabricante
    fabricante: Optional[Fabricante] = None