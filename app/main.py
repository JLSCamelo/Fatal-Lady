from fastapi import FastAPI
from controllers import *
from routes.produto_route import *


app = FastAPI(title="Loja de Sapatos")

app.include_router(router)    