
from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from controllers.endereco_controller import *
from database import get_db

router = APIRouter()
templates = Jinja2Templates(directory="views/templates")


@router.get("/me/enderecos", response_class=HTMLResponse)
def pagina_enderecos(request: Request, db: Session = Depends(get_db)):
    enderecos = listar_enderecos(request, db)
    if isinstance(enderecos, HTMLResponse):
        return enderecos  # redirecionamento de login
    return templates.TemplateResponse(
        "meus_enderecos.html",
        {"request": request, "enderecos": enderecos}
    )


@router.post("/me/enderecos", response_class=HTMLResponse)
def adicionar_endereco(
    request: Request,
    cep: str = Form(...),
    rua: str = Form(...),
    cidade: str = Form(...),
    complemento: str = Form(None),
    db: Session = Depends(get_db)
):
    novo_endereco = criar_endereco(request, db, cep, rua, cidade, complemento)
    if isinstance(novo_endereco, HTMLResponse):
        return novo_endereco  # redirecionamento de login
    return RedirectResponse(url="/me/enderecos", status_code=303)

