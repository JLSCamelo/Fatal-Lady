from fastapi import HTTPException
from fastapi import APIRouter
from typing import List
from controllers.controller_produtos import *
from schemas.produto_schema import *

router = APIRouter(title="Produtos")

@router.get("/produtos", response_model=List[Produto])
async def listar():
    return listar_produto()

@router.post("/criar-produtos", response_model=Produto)
async def criar(produto: ProdutoCreate):
    return criar_produto(produto)

@router.put("/atualizar-produtos/{produto_id}", response_model=Produto)
async def atualizar(produto_id: int, produto: Produto):
    produto_atualizado = atualizar_produto(produto_id, produto)
    if not produto_atualizado:
        raise HTTPException(status_code=404, detail="Produto não encontrado para atualizá-lo.")
    return produto_atualizado

@router.delete("/produto-deletar/{produto_id}")
async def deletar(produto_id: int):
    deletar = deletar_produto(produto_id)
    if not deletar:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return {"mensagem": f"Produto ID: {produto_id} deletado com sucesso."}