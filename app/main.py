<<<<<<< HEAD
from fastapi import FastAPI
from routes.produto_route import router as produto_router
from routes.login_route import router as login_router
from routes.cadastro_route import router as cadastro_router
=======
"""
Nome: Mauricio Bertuci Saletti
DATA: 08/10/2025
RA:24722027
"""

from fastapi import FastAPI
from controllers.controller_produtos import *
from routes.produto_route import *
>>>>>>> 45833ccc4ef94b15890ebafc0aa288548945ec6e
from fastapi.staticfiles import StaticFiles

#montar pasta de imagem
app = FastAPI(title="Loja de Sapatos")

app.mount("/static", StaticFiles(directory="views/static"), name="static")

<<<<<<< HEAD
app.include_router(produto_router)    
app.include_router(login_router)    
app.include_router(cadastro_router)    
=======
app.include_router(router)    
>>>>>>> 45833ccc4ef94b15890ebafc0aa288548945ec6e
