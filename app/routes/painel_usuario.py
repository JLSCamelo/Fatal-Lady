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
    # 1. Tenta obter o token e verificar a autenticação
    token = request.cookies.get("token")
    payload = None # Inicializa payload como None
    
    # ⚡ CORREÇÃO: Verifica se o token existe antes de tentar decodificá-lo
    if token:
        payload = verificar_token(token)
        
    usuario = None
    if payload:
        # 2. Se o token é válido, busca o usuário
        usuario = db.query(UsuarioDB).filter(UsuarioDB.email == payload["sub"]).first()
        
    # 3. Busca os produtos para a seção de destaques (como no seu HTML)
    # Exemplo: (Você precisará adaptar esta parte para o seu modelo de Produto real)
    produtos = db.query(ProdutoDB).all()

    # 4. Renderiza o template, passando o objeto 'usuario' (pode ser o objeto ou None)
    return templates.TemplateResponse("index.html", {
        "request": request,
        "usuario": usuario,  # Passa o usuário logado (ou None)
        "produtos": produtos
    })

# painel do usuario
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

# meus pedidos
@router.get("/me/meus-pedidos", response_class=HTMLResponse)
def meus_pedidos(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("token")
    payload = verificar_token(token)
    if not payload:
        return RedirectResponse(url="/login", status_code=303)
    usuario = db.query(UsuarioDB).filter(UsuarioDB.email == payload["sub"]).first()
    pedidos = db.query(PedidoDB).filter(PedidoDB.id_cliente == usuario.id_cliente).all()
    return templates.TemplateResponse("meus_pedidos.html", {
        "request": request,
        "usuario": usuario,
        "pedidos": pedidos
    })
