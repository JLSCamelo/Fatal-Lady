from fastapi import APIRouter, Form, Depends, Request
from fastapi.responses import HTMLResponse
from database import *
from sqlalchemy.orm import Session
from controllers.carrinho_controller import carrinho_add, carrinho_visualizar, carrinho_update, carrinho_remover


router = APIRouter()

@router.get("/carrinho", response_class=HTMLResponse)
def ver_carrinho(request: Request, db: Session = Depends(get_db)):
    return carrinho_visualizar(request, db)

@router.post("/carrinho.adicionar/{produto_id}")
def adicionar_carrinho(request:Request,
                       produto_id: int,
                       quantidade: int=Form(1),
                       db:Session=Depends(get_db)):
    return carrinho_add(request, produto_id, quantidade, db)

@router.post("/carrinho/editar/{produto_id}")
def editar_quantidade(
    request: Request,
    produto_id: int,
    quantidade: int = Form(...),
    db: Session = Depends(get_db)
):
    return carrinho_update(request, produto_id, quantidade, db)


@router.post("/carrinho/remover/{produto_id}")
def remover_item(
    request: Request,
    produto_id: int,
    db: Session = Depends(get_db)
):
    return carrinho_remover(request, produto_id, db)

    