from pydantic import BaseModel
# from typing import Optional
# from datetime import date

class ProdutoBase(BaseModel): # a base de todos os atributos
    marca: str
    tamanho: int
    estoque: int
    preco: float
    nome: str

class ProdutoCreate(ProdutoBase): # classe usada oara criarmos um produto
    pass

class Produto(ProdutoBase):
    id: int

