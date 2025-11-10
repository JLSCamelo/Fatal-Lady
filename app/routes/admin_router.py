from fastapi import APIRouter, Form, Request, Depends, UploadFile, File, HTTPException
from app.controllers.admin_controller import *
from fastapi.responses import HTMLResponse
from app.database import *
from app.auth import *
from sqlalchemy.orm import Session

router = APIRouter()

#rota admin crud nos produtos
@router.get("/admin",response_class=HTMLResponse)
def get_page_admin(request:Request,db:Session=Depends(get_db)):
    return pagina_admin(request,db)

#rota criar produto
@router.post("/admin/produto/criar")
async def post_produto(
    request: Request,
    nome: str = Form(...),
    preco: float = Form(...),
    estoque: int = Form(...),
    id_fabricante: int = Form(...),
    id_categoria: int = Form(...),
    tamanho: int = Form(...),
    imagem: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    return criar_produto(request, nome, preco, estoque, id_fabricante , id_categoria, tamanho,imagem, db)

#editar produto
@router.get("/admin/produto/editar/{id}")
def get_editar_produto(id:int, request: Request,db:Session=Depends(get_db)):
   return editar_produto(id,request,db)

#rota atualzar produto post
@router.post("/admin/produto/atualizar/{id}")
def get_atualizar_produto(id:int,nome:str=Form(...),
                      preco:float=Form(...), estoque:int=Form(...),
                      imagem:UploadFile=File(None),db:Session=Depends(get_db)):
    return atualizar_produto(id,nome,preco,estoque,imagem,db)
   

#deletar produto
@router.post("/admin/produto/deletar/{id}")
def delete_produto(id:int,db:Session=Depends(get_db)):
    return deletar_produto(id,db)
