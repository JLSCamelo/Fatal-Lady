from fastapi import FastAPI
from routes.produto_route import router as produto_router
from routes.login_route import router as login_router
from routes.cadastro_route import router as cadastro_router
from routes.carrinho_router import router as carrinho_router
from routes.checkout_router import router as checkout_router
from fastapi.staticfiles import StaticFiles
from database import Base, engine
from models import *

Base.metadata.create_all(bind=engine)


app = FastAPI(title="Loja de Sapatos")

app.mount("/static", StaticFiles(directory="views/static"), name="static")

app.include_router(produto_router)    
app.include_router(login_router)    
app.include_router(cadastro_router)    

 
