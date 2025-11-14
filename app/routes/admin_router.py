from fastapi import APIRouter, Form, Request, Depends, UploadFile, File, HTTPException
from app.controllers.admin_controller import *
from fastapi.responses import HTMLResponse
from app.database import *
from app.auth import *
from sqlalchemy.orm import Session

router = APIRouter(prefix="/admin")

#rota admin crud nos produtos
@router.get("/",response_class=HTMLResponse)
def page(request:Request,db:Session=Depends(get_db)):
    return pagina_admin(request,db)

#rota criar produto
@router.post("/produto/criar")
async def create(
    request: Request,
    nome: str = Form(...),
    preco: float = Form(...),
    estoque: int = Form(...),
    id_fabricante: int = Form(...),
    id_categoria: int = Form(...),
    tamanho: str = Form(...),
    imagem: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    return criar_produto(request, nome, preco, estoque, id_fabricante , id_categoria, tamanho,imagem, db)

#editar produto
@router.get("/produto/editar/{id}")
def page_update(id:int, request: Request,db:Session=Depends(get_db)):
   return editar_produto(id,request,db)

#rota atualzar produto post
@router.post("/produto/atualizar/{id}")
def updade(id:int,nome:str=Form(...),
                      preco:float=Form(...), estoque:int=Form(...),
                      imagem:UploadFile=File(None),db:Session=Depends(get_db)):
    return atualizar_produto(id,nome,preco,estoque,imagem,db)
   

#deletar produto
@router.post("/produto/deletar/{id}")
def delete(id:int,db:Session=Depends(get_db)):
    return deletar_produto(id,db)
