from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import Optional

from sqlalchemy.orm import Session
from app.controllers.endereco_controller import (
    listar_enderecos,
    salvar_endereco,
    definir_endereco_principal,
    remover_endereco,
)
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
            "endereco": dados["enderecos"],
        },
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
    destinatario: str = Form(...),
    principal: Optional[bool] = Form(None),
    endereco_id: Optional[int] = Form(None),
    db: Session = Depends(get_db),
):
    novo_endereco = salvar_endereco(
        request,
        cep,
        rua,
        bairro,
        cidade,
        estado,
        complemento,
        numero,
        apelido,
        destinatario,
        principal,
        db,
        endereco_id,
    )
    if isinstance(novo_endereco, HTMLResponse):
        return novo_endereco
    return RedirectResponse(url="/me/enderecos", status_code=303)

@router.patch("/me/enderecos/{endereco_id}/principal")
def set_endereco_principal(request: Request, endereco_id: int, db: Session = Depends(get_db)):
    return definir_endereco_principal(request, endereco_id, db)


@router.delete("/me/enderecos/{endereco_id}")
def delete_endereco(request: Request, endereco_id: int, db: Session = Depends(get_db)):
    return remover_endereco(request, endereco_id, db)
