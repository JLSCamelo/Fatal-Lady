from fastapi import APIRouter, Form, Depends, Request
from fastapi.responses import HTMLResponse
from database import *
from sqlalchemy.orm import Session
from controllers.carrinho_controller import carrinho_add, carrinho_visualizar, carrinho_update, carrinho_remover
from fastapi.templating import Jinja2Templates
from auth import verificar_token
from database import get_db
from models import UsuarioDB

router = APIRouter()
templates = Jinja2Templates(directory="views/templates")

@router.get("/carrinho", response_class=HTMLResponse)
def get_carrinho(request: Request, db: Session = Depends(get_db)):
    # A rota agora simplesmente chama o controller, que faz todo o trabalho.
    return carrinho_visualizar(request, db)

@router.post("/carrinho/adicionar/{produto_id}")
def post_carrinho(request:Request,
                       produto_id: int,
                       quantidade: int=Form(1),
                       tamanho: int=Form(...),
                       db:Session=Depends(get_db)):
    return carrinho_add(request, produto_id, quantidade, tamanho, db)

@router.post("/carrinho/editar/{produto_id}")
def put_carrinho(
    request: Request,
    produto_id: int,
    quantidade: int = Form(...),
    db: Session = Depends(get_db)
):
    return carrinho_update(request, produto_id, quantidade, db)


@router.post("/carrinho/remover/{produto_id}")
def delete_item_carrinho(
    request: Request,
    produto_id: int,
    db: Session = Depends(get_db)
):
    return carrinho_remover(request, produto_id, db)