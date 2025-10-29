from fastapi import APIRouter, Request, Form, UploadFile, File, Depends 
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os, shutil
from sqlalchemy.orm import Session
from database import get_db
from controllers.produtos_controller import *

router = APIRouter() #rotas
templates = Jinja2Templates(directory="views/templates") #front-end

#pasta para dalvar imagens
UPLOAD_DIR= "views/static/uploads"
#caminhos para o os
os.makedirs(UPLOAD_DIR,exist_ok=True)

#rota home pagaina inicial
@router.get("/", response_class=HTMLResponse)
async def get_home(request: Request):
    produtos = listar_produto()
    return templates.TemplateResponse("index.html",{
        "request": request, "produtos": produtos
    })

#rota para pagina listar produtos
@router.get("/produtos", response_class=HTMLResponse)
async def get_listar_produtos(request: Request):
    produtos = listar_produto()
    return templates.TemplateResponse("catalogo.html", {
        "request": request, "produtos":produtos
    })

@router.get("/categoria", response_class=HTMLResponse)
async def get_produtos_categoria(request: Request):
    produtos = produtos_por_categoria()
    return templates.TemplateResponse("catalogo.html", {
        "request": request, "produtos":produtos
    })

#rota para detalhar produto
@router.get("/produto-get/{id_produto}", response_class=HTMLResponse)
async def get_detalhe_produto(request:Request, id_produto:int):
        produto = get_produto(id_produto)
        return templates.TemplateResponse("produto.html",{
        "request":request, "produto":produto
    })

