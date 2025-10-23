from fastapi import APIRouter, Form, Depends, Request
from database import *
from sqlalchemy.orm import Session
from controllers.carrinho_controller import carrinho_controller
from fastapi.templating import Jinja2Templates


router = APIRouter()
templates = Jinja2Templates(directory="views/templates")


@router.post("/carrinho.adicionar/{produto_id}")
def adicionar_carrinho(request:Request,
                       produto_id: int,
                       quantidade: int=Form(1),
                       db:Session=Depends(get_db)):
    return carrinho_controller(produto_id, quantidade, db)
    