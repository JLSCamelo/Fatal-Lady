from fastapi import Form, Request, UploadFile, File
from fastapi.responses import RedirectResponse
import os, shutil
from database import *
from models.produto_model import ProdutoDB
from models.categoria_model import CategoriaDB
from fastapi.templating import Jinja2Templates
from auth import *
from sqlalchemy.orm import Session

templates =Jinja2Templates(directory="views/templates")
UPLOAD_DIR="views/static/uploads/img"
#caminho para o os
os.makedirs(UPLOAD_DIR,exist_ok=True)


def pagina_admin(request:Request,db:Session):
    token=request.cookies.get("token")
    payload=verificar_token(token)

    if not payload or not payload.get("is_admin"):
        return RedirectResponse(url="/",status_code=303)
    
    produtos=db.query(ProdutoDB).all()
    
    return templates.TemplateResponse("admin.html",{
        "request":request,"produtos":produtos
    })

def criar_produto(request: Request, 
                  nome: str, 
                  preco: float, 
                  quantidade: int, 
                  id_fabricante: int,
                  id_categoria: int, 
                  tamanhos: int,
                  imagem: UploadFile, 
                  nome_categoria : str,
                  db: Session):
    caminho_arquivo = None

    if imagem and imagem.filename:
        caminho_arquivo = os.path.join(UPLOAD_DIR, imagem.filename)
        with open(caminho_arquivo, "wb") as arquivo:
           shutil.copyfileobj(imagem.file,arquivo)

    novo_produto = ProdutoDB(
        nome=nome,
        preco=preco,
        estoque=quantidade,
        fabricante = id_fabricante,
        categoria=id_categoria,
        tamanhos = tamanhos,
        imagem=caminho_arquivo,
        nome_categoria = nome_categoria
    )

    db.add(novo_produto)
    db.commit()
    db.refresh(novo_produto)

    return RedirectResponse(url="/admin", status_code=303)

def editar_produto(id:int, request: Request,db:Session):
    token = request.cookies.get("token")
    payload = verificar_token(token)

    if not payload or payload.get("is_admin"):
        return RedirectResponse(url="/",status_code=303)
    
    produto = db.query(ProdutoDB).filter(ProdutoDB.id_produto==id).first()
    if not produto:
        return RedirectResponse(url="/admin",status_code=303)
    
    return templates.TemplateResponse("editar.html",{
        "request":request, "produto":produto
    })

def atualizar_produto(id:int,nome:str,
                      preco:float, quantidade:int,
                      imagem:UploadFile,db:Session):
    
    produto = db.query(ProdutoDB).filter(ProdutoDB.id_produto==id).first()
    if not produto:
        return RedirectResponse(url="/admin", status_code=303)
    
    #atualizar campos
    produto.nome = nome
    produto.preco = preco
    produto.estoque = quantidade
    #atualizar image se uma nova for enviada
    if imagem and imagem.filename !="":
        caminho_arquivo=f"{UPLOAD_DIR}/{imagem.filename}"
        with open(caminho_arquivo,"wb") as arquivo:
            shutil.copyfileobj(imagem.file,arquivo)
        produto.caminhoimagem=imagem.filename
        db.commit()
        db.refresh(produto)
        return RedirectResponse(url="/admin",status_code=303)

def deletar_produto(id:int,db:Session):
    produto=db.query(ProdutoDB).filter(ProdutoDB.id_produto==id).first()

    if produto:
        db.delete(produto)
        db.commit()

    return RedirectResponse(url="/admin",status_code=303)
