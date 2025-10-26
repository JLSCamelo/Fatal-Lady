from fastapi import APIRouter, Form, Depends, Request
from fastapi.responses import HTMLResponse
from database import *
from sqlalchemy.orm import Session
from controllers.carrinho_controller import carrinho_add, carrinho_visualizar


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
    