from pydantic import BaseModel
from typing import List, Optional

# ---------- CATEGORIA ----------
class CategoriaBase(BaseModel):
    nome: str
    descricao: Optional[str] = None

class CategoriaCreate(CategoriaBase):
    pass

class CategoriaUpdate(BaseModel):
    nome: Optional[str] = None
    descricao: Optional[str] = None

class Categoria(CategoriaBase):
    id: int
    # produtos: List[Produto] = []  # Opcional: incluir produtos se necessário

    class Config:
        from_attributes = True
