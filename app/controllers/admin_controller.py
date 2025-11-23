from fastapi import Form, Request, UploadFile, File
from fastapi.responses import RedirectResponse
import os, shutil
from app.database import *
from app.models.produto_model import ProdutoDB
from app.models.categoria_model import CategoriaDB
from app.models.fabricante_model import FabricanteDB

# para a coluna de pagamentos
from app.models.pagamento_model import PagamentoDB
from app.models.pedido_model import PedidoDB
from app.models.usuario_model import UsuarioDB

from fastapi.templating import Jinja2Templates
from app.auth import *
from sqlalchemy.orm import Session, joinedload

templates =Jinja2Templates(directory="app/views/templates")
UPLOAD_DIR="app/views/static/uploads/img"
#caminho para o os
os.makedirs(UPLOAD_DIR,exist_ok=True)


def pagina_admin(request:Request,db:Session):
    token=request.cookies.get("token")
    payload=verificar_token(token)

    if not payload or not payload.get("is_admin"):
        return RedirectResponse(url="/",status_code=303)
    
    produtos=db.query(ProdutoDB).all()
    categorias = db.query(CategoriaDB).all()
    fabricantes = db.query(FabricanteDB).all()

    pagamentos = (
        db.query(PagamentoDB)
        .options(
            joinedload(PagamentoDB.pedido).joinedload(PedidoDB.usuario)
        )
        .order_by(PagamentoDB.data_criacao.desc())
        .all()
    )


    return templates.TemplateResponse(
        "admin.html",
        {
            "request": request,
            "produtos": produtos,
            "categorias": categorias,
            "fabricantes": fabricantes,
            "pagamentos": pagamentos,
        },
    )
    
    return templates.TemplateResponse("admin.html",{
        "request":request,"produtos":produtos, "categorias":categorias, "fabricantes": fabricantes 
    })

def criar_produto(request: Request, 
                  nome: str, 
                  preco: float, 
                  estoque: int, 
                  id_fabricante: int,
                  id_categoria: int, 
                  tamanhos: str,
                  imagem: UploadFile, 
                  db: Session):
    caminho_arquivo = None

    if imagem and imagem.filename:
        caminho_arquivo = os.path.join(UPLOAD_DIR, imagem.filename)
        with open(caminho_arquivo, "wb") as arquivo:
           shutil.copyfileobj(imagem.file,arquivo)

    novo_produto = ProdutoDB(
        nome=nome,
        preco=preco,
        estoque=estoque,
        id_fabricante = id_fabricante,
        id_categoria=id_categoria,
        tamanhos = tamanhos,
        caminhoimagem=caminho_arquivo,
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
                      preco:float, estoque:int,
                      imagem:UploadFile,db:Session):
    
    produto = db.query(ProdutoDB).filter(ProdutoDB.id_produto==id).first()
    if not produto:
        return RedirectResponse(url="/admin", status_code=303)
    
    #atualizar campos
    produto.nome = nome
    produto.preco = preco
    produto.estoque = estoque
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
