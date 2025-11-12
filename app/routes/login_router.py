# routes/login_router.py
import json
from fastapi import APIRouter, Request, Form, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import get_db
from app.controllers.login_controller import login_controller
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi import Request

# login com facebook e google =========================
from app.oauth_config import oauth
from authlib.integrations.starlette_client import OAuth
from starlette.requests import Request as LoginStarlette
import os

from app.auth import criar_token
from app.models.usuario_model import UsuarioDB

router = APIRouter()
templates = Jinja2Templates(directory="app/views/templates")

@router.get("/login",response_class=HTMLResponse)
def page(request:Request):
    return templates.TemplateResponse("login.html",{
        "request":request
    })

@router.post("/login")
def logar(request: Request,
               email: str = Form(...),
               senha: str = Form(...),
               db: Session = Depends(get_db)):
    return login_controller(request, email, senha, db)




#############################################################
#Verificar
# rota para iniciar login Google
# @router.get("/login/google")
# async def login_google(request: LoginStarlette):
#     redirect_uri = request.url_for("auth_google_callback")
#     return await oauth.google.authorize_redirect(request, redirect_uri)

# # rota de retorno Google
# @router.get("/auth/google/callback", name="auth_google_callback")
# async def auth_google_callback(request: LoginStarlette, db: Session = Depends(get_db)):
#     # Aqui valida o state e pega o token
#     token = await oauth.google.authorize_access_token(request)
    
#     # Pega informações do usuário (Google ID token)
#     user = await oauth.google.parse_id_token(request, token)
    
#     email = user.get("email")
#     nome = user.get("name", "")
    
#     # Cria ou busca usuário no DB
#     usuario = db.query(UsuarioDB).filter_by(email=email).first()
#     if not usuario:
#         usuario = UsuarioDB(email=email, nome=nome, senha="")
#         db.add(usuario)
#         db.commit()
#         db.refresh(usuario)
    
#     # Cria JWT e seta cookie
#     jwt = criar_token({"sub": usuario.email})
#     response = RedirectResponse(url="/")
#     response.set_cookie(key="token", value=jwt, httponly=True)
#     return response

# =================
# FACEBOOK ---- NAO TA UNCIONANDO!! 😭
# =================

oauth = OAuth()
oauth.register(
    name="facebook",
    client_id=os.getenv("FACEBOOK_CLIENT_ID"),
    client_secret=os.getenv("FACEBOOK_CLIENT_SECRET"),
    access_token_url="https://graph.facebook.com/v12.0/oauth/access_token",
    access_token_params=None,
    authorize_url="https://www.facebook.com/v12.0/dialog/oauth",
    authorize_params=None,
    api_base_url="https://graph.facebook.com/v12.0/",
    client_kwargs={"scope": "email public_profile"},
)

# redireciona para facebook
@router.get("/auth/facebook") # Seu HTML precisa ter <a href="/auth/facebook">
async def auth_facebook(request: Request):
    # Usando request.url_for para ser mais seguro e automático
    redirect_uri = request.url_for('auth_facebook_callback')
    return await oauth.facebook.authorize_redirect(request, str(redirect_uri))

# callback — retorna do facebook
@router.get("/auth/facebook/callback", name="auth_facebook_callback")
async def auth_facebook_callback(request: Request, db: Session = Depends(get_db)): # <-- PROBLEMA 3 CORRIGIDO
    
    try:
        token = await oauth.facebook.authorize_access_token(request)
    except Exception as e:
        # <-- PROBLEMA 1 CORRIGIDO (access_denied)
        # Se o usuário clicar em "Cancelar", o erro cai aqui
        print(f"Usuário cancelou ou deu erro: {e}")
        return RedirectResponse(url="/login") # Manda de volta pro login

    # Se o 'try' funcionou, o usuário logou.
    user_info = await oauth.facebook.get("me?fields=id,name,email", token=token)
    user_data = user_info.json()

    email = user_data.get("email")
    nome = user_data.get("name")

    if not email:
        # Se o Facebook não retornar o e-mail
        return RedirectResponse(url="/login?error=email_nao_fornecido")

    # salvar ou buscar o usuário no banco (usando o 'db' injetado)
    usuario = db.query(UsuarioDB).filter(UsuarioDB.email == email).first()

    if not usuario:
        # Use "" para a senha, já que o usuário não tem uma
        novo = UsuarioDB(nome=nome, email=email, senha="") 
        db.add(novo)
        db.commit()
        db.refresh(novo)
        usuario = novo
    
    # (Não precisa de db.close(), o Depends(get_db) cuida disso)

    # cookie/token de sessão
    jwt = criar_token({"sub": usuario.email}) # <-- PROBLEMA 4 CORRIGIDO (Segurança)
    response = RedirectResponse(url="/me/painel", status_code=303)
    response.set_cookie(key="token", value=jwt, httponly=True) # Salva o token JWT

    return response




# @router.get("/login/facebook")
# async def login_facebook(request: Request):
#     print("=" * 50)
#     print("INICIANDO LOGIN FACEBOOK")
#     print(f"Cookies recebidos: {request.cookies}")
#     print(f"Session ANTES do redirect: {dict(request.session)}") # Para saber se está sendo recebido e redirecionado
    
#     redirect_uri = request.url_for('auth/facebook/callback')
#     response = await oauth.facebook.authorize_redirect(request, redirect_uri)
    
#     print(f"Session DEPOIS do redirect: {dict(request.session)}")
#     print(f"Cookies na resposta: {response.headers.get('set-cookie')}")
#     print("=" * 50)
    
#     return response

# @router.get("/auth/facebook/callback")
# async def auth_facebook_callback(request: Request, db: Session = Depends(get_db)):
#     print("=" * 50)
#     print("CALLBACK FACEBOOK RECEBIDO")
#     print(f"Query params: {request.query_params}")
#     print(f"Session: {request.session}")
#     print("=" * 50)
    
#     try:
#         token = await oauth.facebook.authorize_access_token(request)
#     except Exception as e:
#         print("!!! ERRO NO CALLBACK DO FACEBOOK !!!")
#         print(f"Tipo do erro: {type(e)}")
#         print(f"Mensagem: {e}")
#         return RedirectResponse(url="/login?error=facebook-cancelado")
    
#     resp = await oauth.facebook.get('me?fields=id,name,email')
#     user_info = resp.json()
    
#     email = user_info.get("email")
#     nome = user_info.get("name")
    
#     # Se o Facebook não retornar um e-mail (raro, mas pode acontecer)
#     if not email:
#         return RedirectResponse(url="/login?error=facebook-no-email")
#     # ---------------------------------

#     # Cria ou busca usuário no DB 
#     usuario = db.query(UsuarioDB).filter_by(email=email).first()
    
#     if not usuario:
#         usuario = UsuarioDB(email=email, nome=nome, senha="") 
#         db.add(usuario)
#         db.commit()
#         db.refresh(usuario) # Garante que o ID do usuário está carregado

#     # Cria JWT e seta cookie (Seu código aqui estava bom)
#     jwt = criar_token({"sub": usuario.email})
    
#     response = RedirectResponse(url="/")
#     response.set_cookie(key="token", value=jwt, httponly=True)
    
#     return response