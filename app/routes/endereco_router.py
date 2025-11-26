from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import Optional
from starlette.responses import Response

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

    if isinstance(dados, Response):
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
    endereco_id: Optional[str] = Form(None),
    db: Session = Depends(get_db),
):
    endereco_id_int = int(endereco_id) if endereco_id not in (None, "", "null") else None

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
        endereco_id_int,
    )
    if isinstance(novo_endereco, HTMLResponse):
        return novo_endereco
    return RedirectResponse(url="/me/enderecos", status_code=303)

@router.post("/me/enderecos/{endereco_id}/principal")
def set_endereco_principal(request: Request, endereco_id: int, db: Session = Depends(get_db)):
    return definir_endereco_principal(request, endereco_id, db)


@router.delete("/me/enderecos/{endereco_id}/deletar")
def delete_endereco(request: Request, endereco_id: int, db: Session = Depends(get_db)):
    return remover_endereco(request, endereco_id, db)
