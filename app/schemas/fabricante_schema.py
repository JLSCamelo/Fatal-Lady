from pydantic import BaseModel, EmailStr, validator
from typing import Optional, List
import re

# ---------- SCHEMAS BASE ----------
class FabricanteBase(BaseModel):
    nome: str
    descricao: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None
    pais: Optional[str] = "Brasil"
    cnpj: Optional[str] = None
    telefone: Optional[str] = None
    email: Optional[EmailStr] = None

class FabricanteCreate(FabricanteBase):
    @validator('nome')
    def nome_nao_vazio(cls, v):
        if not v or not v.strip():
            raise ValueError('O nome não pode ser vazio')
        return v.strip()
    
    @validator('cnpj')
    def cnpj_valido(cls, v):
        if v:
            # Remove caracteres não numéricos
            cnpj_limpo = re.sub(r'\D', '', v)
            if len(cnpj_limpo) != 14:
                raise ValueError('CNPJ deve ter 14 dígitos')
        return v
    
    @validator('telefone')
    def telefone_valido(cls, v):
        if v:
            telefone_limpo = re.sub(r'\D', '', v)
            if len(telefone_limpo) < 10:
                raise ValueError('Telefone deve ter pelo menos 10 dígitos')
        return v

class FabricanteUpdate(BaseModel):
    nome: Optional[str] = None
    descricao: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None
    pais: Optional[str] = None
    cnpj: Optional[str] = None
    telefone: Optional[str] = None
    email: Optional[EmailStr] = None
    ativo: Optional[int] = None

# ---------- SCHEMAS DE RESPOSTA ----------
class Fabricante(FabricanteBase):
    id: int
    ativo: int

    class Config:
        from_attributes = True

class FabricanteComProdutos(Fabricante):
    from app.schemas.produto_schema import Produto  # Import condicional
    produtos: List[Produto] = []

    class Config:
        from_attributes = True

# ---------- SCHEMAS PARA LISTAGEM ----------
class FabricanteResumo(BaseModel):
    id: int
    nome: str
    cidade: Optional[str] = None
    estado: Optional[str] = None

    class Config:
        from_attributes = True