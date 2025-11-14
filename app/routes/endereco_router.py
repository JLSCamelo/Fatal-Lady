from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.controllers.endereco_controller import listar_enderecos, criar_endereco
from app.database import get_db

router = APIRouter()
templates = Jinja2Templates(directory="app/views/templates")


@router.get("/me/enderecos", response_class=HTMLResponse)
def page_enderecos(request: Request, db: Session = Depends(get_db)):
    dados = listar_enderecos(request, db)

    if isinstance(dados, HTMLResponse):
        return dados  # redireciona login

    return templates.TemplateResponse(
        "meus_endereços.html",
        {
            "request": request,
            "usuario": dados["usuario"],
            "endereco": dados["enderecos"]  
        }
    )


@router.post("/me/criar/enderecos", response_class=HTMLResponse)
def add_endereco(
    request: Request,
    cep: str = Form(...),
    rua: str = Form(...),
    bairro: str = Form(...),
    cidade: str = Form(...),
    estado: str = Form(...),
    complemento: str = Form(None),
    numero: str = Form(...),
    apelido: str = Form(...),
    db: Session = Depends(get_db)
):
    novo_endereco = criar_endereco(request, db, cep, rua, bairro, cidade, estado, complemento, numero, apelido)

    if isinstance(novo_endereco, HTMLResponse):
        return novo_endereco

    return RedirectResponse(url="/me/enderecos", status_code=303)
