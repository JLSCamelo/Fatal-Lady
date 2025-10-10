"""
Nome: Mauricio Bertuci Saletti
DATA: 08/10/2025
RA:24722027
"""

from fastapi import FastAPI
from controllers.controller_produtos import *
from routes.produto_route import *
from fastapi.staticfiles import StaticFiles

#montar pasta de imagem
app = FastAPI(title="Loja de Sapatos")

app.mount("/static", StaticFiles(directory="views/static"), name="static")

app.include_router(router)    