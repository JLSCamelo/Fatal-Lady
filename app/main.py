from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
# login google e facebook
from starlette.middleware.sessions import SessionMiddleware
from dotenv import load_dotenv
import os

from routes.produto_router import router as produto_router
from routes.login_router import router as login_router
from routes.cadastro_router import router as cadastro_router
from routes.carrinho_router import router as carrinho_router
from routes.checkout_router import router as checkout_router
from routes.meus_pedidos_router import router as meus_pedidos_router
from routes.logout_router import router as logout_router
from routes.admin_router import router as admin_router
from routes.categoria_router import router as categoria_router
from routes.painel_usuario import router as painel_usuario_router
from database import Base, engine
from models import *


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Loja de Sapatos")

# usado para login com google e facebook (antes das rotas)
load_dotenv()
app.add_middleware(
    SessionMiddleware,
    secret_key= os.getenv("SECRET_KEY", "FATALLADY@134"),  
    same_site="lax", 
    https_only=False,
    max_age=3600
)


app.mount("/static", StaticFiles(directory="views/static"), name="static")

app.include_router(produto_router)    
app.include_router(login_router)    
app.include_router(cadastro_router)
app.include_router(carrinho_router)   
app.include_router(checkout_router)   
app.include_router(meus_pedidos_router)   
app.include_router(admin_router)   
app.include_router(painel_usuario_router)   
app.include_router(logout_router)   
app.include_router(categoria_router)
 
