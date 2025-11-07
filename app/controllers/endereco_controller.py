from fastapi import Form, Request, File
from fastapi.responses import RedirectResponse
import os, shutil
from database import *
from models.usuario_model import UsuarioDB
from fastapi.templating import Jinja2Templates
from auth import *
from sqlalchemy.orm import Session

templates =Jinja2Templates(directory="views/templates")
UPLOAD_DIR="views/static/uploads/img"
#caminho para o os
os.makedirs(UPLOAD_DIR,exist_ok=True)


def pagina_endereco(request:Request,db:Session):
    token=request.cookies.get("token")
    payload=verificar_token(token)

    if not payload or not payload.get("is_admin"):
        return RedirectResponse(url="/",status_code=303)
    
    produtos=db.query(UsuarioDB).all()
    categorias = db.query(CategoriaDB).all()
    
    return templates.TemplateResponse("admin.html",{
        "request":request,"produtos":produtos, "categorias":categorias
    })


def editar_endereco(id:int, request: Request,db:Session):
    token = request.cookies.get("token")
    payload = verificar_token(token)

    if not payload or payload.get("is_admin"):
        return RedirectResponse(url="/",status_code=303)
    
    produto = db.query(UsuarioDB).filter(UsuarioDB.id_produto==id).first()
    if not produto:
        return RedirectResponse(url="/admin",status_code=303)
    
    return templates.TemplateResponse("editar.html",{
        "request":request, "produto":produto
    })

def deletar_endereco(id:int,db:Session):
    endereco=db.query(UsuarioDB).filter(UsuarioDB.id_produto==id).first()

    if produto:
        db.delete(produto)
        db.commit()

    return RedirectResponse(url="/admin",status_code=303)
