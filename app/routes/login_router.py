# routes/login_route.py
import json
from fastapi import APIRouter, Request, Form, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import get_db
from controllers.login_controller import login_controller
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi import Request

from oauth_config import oauth
from starlette.requests import Request as LoginStarlette

from auth import criar_token
from models.usuario_model import UsuarioDB
router = APIRouter()
templates = Jinja2Templates(directory="views/templates")

@router.get("/login",response_class=HTMLResponse)
def home(request:Request):
    return templates.TemplateResponse("login.html",{
        "request":request
    })

@router.post("/login")
def post_login(request: Request,
               email: str = Form(...),
               senha: str = Form(...),
               db: Session = Depends(get_db)):
    return login_controller(request, email, senha, db)




#############################################################
#Verificar
# rota para iniciar login Google
@router.get("/login/google")
async def login_google(request: LoginStarlette):
    redirect_uri = request.url_for("auth_google_callback")
    return await oauth.google.authorize_redirect(request, redirect_uri)

# rota de retorno Google
@router.get("/auth/google/callback", name="auth_google_callback")
async def auth_google_callback(request: LoginStarlette, db: Session = Depends(get_db)):
    # Aqui valida o state e pega o token
    token = await oauth.google.authorize_access_token(request)
    
    # Pega informações do usuário (Google ID token)
    user = await oauth.google.parse_id_token(request, token)
    
    email = user.get("email")
    nome = user.get("name", "")
    
    # Cria ou busca usuário no DB
    usuario = db.query(UsuarioDB).filter_by(email=email).first()
    if not usuario:
        usuario = UsuarioDB(email=email, nome=nome, senha="")
        db.add(usuario)
        db.commit()
        db.refresh(usuario)
    
    # Cria JWT e seta cookie
    jwt = criar_token({"sub": usuario.email})
    response = RedirectResponse(url="/")
    response.set_cookie(key="token", value=jwt, httponly=True)
    return response

# ====== FACEBOOK ======
@router.get("/login/facebook")
async def login_facebook(request: LoginStarlette):
    redirect_uri = request.url_for("auth_facebook_callback")
    return await oauth.facebook.authorize_redirect(request, redirect_uri)

@router.get("/auth/facebook/callback")
async def auth_facebook_callback(request: LoginStarlette, db: Session = Depends(get_db)):
       # Aqui valida o state e pega o token
    token = await oauth.facebook.authorize_access_token(request)
    
    # Pega informações do usuário (Google ID token)
    user = await oauth.facebook.parse_id_token(request, token)
    
    email = user.get("email")
    nome = user.get("name", "")
    
    # Cria ou busca usuário no DB
    usuario = db.query(UsuarioDB).filter_by(email=email).first()
    if not usuario:
        usuario = UsuarioDB(email=email, nome=nome, senha="")
        db.add(usuario)
        db.commit()
    
    # Cria JWT e seta cookie
    jwt = criar_token({"sub": usuario.email})
    response = RedirectResponse(url="/")
    response.set_cookie(key="token", value=jwt, httponly=True)
    return response
