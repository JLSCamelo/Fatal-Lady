from fastapi import APIRouter, Form, Depends, Request
from fastapi.responses import HTMLResponse
from database import *
from sqlalchemy.orm import Session
from controllers.carrinho_controller import carrinho_add, carrinho_visualizar, carrinho_update, carrinho_remover
from fastapi.templating import Jinja2Templates
from database import get_db

router = APIRouter()
templates = Jinja2Templates(directory="views/templates")

@router.get("/carrinho", response_class=HTMLResponse)
def get_carrinho(request: Request, db: Session = Depends(get_db)):
    return carrinho_visualizar(request, db)

@router.post("/carrinho/adicionar/{produto_id}")
def post_carrinho(request:Request,
                       produto_id: int,
                       tamanho: int=Form(...),
                        quantidade: int=Form(1),
                       db:Session=Depends(get_db)
):
    return carrinho_add(request, produto_id, quantidade, tamanho, db)

@router.post("/carrinho/editar/{produto_id}")
def put_carrinho(
    request: Request,
    produto_id: int,
    tamanho: int = Form(...),
    quantidade: int = Form(...),
    db: Session = Depends(get_db)
):
    return carrinho_update(
    request=request,
    produto_id=produto_id,
    tamanho=tamanho,
    quantidade=quantidade,
    db=db
)


@router.post("/carrinho/remover/{produto_id}")
def delete_item_carrinho(
    request: Request,
    produto_id: int,
    db: Session = Depends(get_db)
):
    return carrinho_remover(request, produto_id, db)