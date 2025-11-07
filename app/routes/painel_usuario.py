from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from auth import verificar_token
from database import get_db
from models import UsuarioDB, PedidoDB, ProdutoDB

router = APIRouter()
templates = Jinja2Templates(directory="views/templates")

@router.get("/", response_class=HTMLResponse)
def home(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("token")
    payload = None
    
    if token:
        payload = verificar_token(token)
        
    usuario = None
    if payload:
        usuario = db.query(UsuarioDB).filter(UsuarioDB.email == payload["sub"]).first()

    produtos = db.query(ProdutoDB).all()

    return templates.TemplateResponse("index.html", {
        "request": request,
        "usuario": usuario, 
        "produtos": produtos
    })


@router.get("/me/painel", response_class=HTMLResponse)
def painel_usuario(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("token")
    payload = verificar_token(token)
    if not payload:
        return RedirectResponse(url="/login", status_code=303)
    usuario = db.query(UsuarioDB).filter(UsuarioDB.email == payload["sub"]).first()
    if not usuario:
        return RedirectResponse(url="/login", status_code=303)
    pedidos = db.query(PedidoDB).filter(PedidoDB.id_cliente == usuario.id_cliente).all()
    return templates.TemplateResponse("painel_usuario.html", {
        "request": request,
        "usuario": usuario,
        "pedidos": pedidos
    })

# dados
@router.get("/me/dados", response_class=HTMLResponse)
def meus_dados(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("token")
    payload = verificar_token(token)
    if not payload:
        return RedirectResponse(url="/login", status_code=303)
    usuario = db.query(UsuarioDB).filter(UsuarioDB.email == payload["sub"]).first()
    return templates.TemplateResponse("meus_dados.html", {
        "request": request,
        "usuario": usuario
    })

@router.get("/me/enderecos", response_class=HTMLResponse)
def listar_endereco_usuario(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("token")
    if not token:
        return RedirectResponse(url="/login", status_code=303)

    payload = verificar_token(token)
    if not payload:
        return RedirectResponse(url="/login", status_code=303)

    email = payload.get("sub")

    usuario = db.query(UsuarioDB).filter_by(email=email).first()
    if not usuario:
        return RedirectResponse(url="/login", status_code=303)

    endereco = {
        "rua": usuario.rua,
        "cidade": usuario.cidade,
        "cep": usuario.cep,
        "complemento": usuario.complemento,
    }

    return templates.TemplateResponse(
        "meus_endereços.html",
        {
            "request": request,
            "usuario": usuario,
            "endereco": endereco
        }
    )




#remove o cookie do token do usuário
@router.get("/logout")
def logout(request:Request):
    response=RedirectResponse(url="/",status_code=303)
    response.delete_cookie(key="token")
    return response