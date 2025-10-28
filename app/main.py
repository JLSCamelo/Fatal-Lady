from fastapi import FastAPI
from routes.produto_router import router as produto_router
from routes.login_router import router as login_router
from routes.cadastro_router import router as cadastro_router
from routes.carrinho_router import router as carrinho_router
from routes.checkout_router import router as checkout_router
from routes.meus_pedidos_router import router as meus_pedidos_router
from routes.logout_router import router as logout_router
from routes.admin_router import router as admin_router
from fastapi.staticfiles import StaticFiles
from database import Base, engine
from models import *

# usado para login com google e facebook
from starlette.middleware.sessions import SessionMiddleware

Base.metadata.create_all(bind=engine)


app = FastAPI(title="Loja de Sapatos")

# Adicione ANTES das rotas
app.add_middleware(
    SessionMiddleware,
    secret_key="FaltaLadyProject2025",
    same_site="lax",  # evita bloqueio de cookies
    https_only=False,  # True em produção (HTTPS)
)

app.mount("/static", StaticFiles(directory="views/static"), name="static")

app.include_router(produto_router)    
app.include_router(login_router)    
app.include_router(cadastro_router)
app.include_router(carrinho_router)   
app.include_router(checkout_router)   
app.include_router(meus_pedidos_router)   
app.include_router(admin_router)   
app.include_router(logout_router)   

 
