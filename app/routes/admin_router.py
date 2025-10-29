from fastapi import APIRouter, Form, Request, Depends, UploadFile, File, HTTPException
from controllers.admin_controller import *
from fastapi.responses import HTMLResponse
from database import *
from auth import *
from sqlalchemy.orm import Session

router = APIRouter()

#rota admin crud nos produtos
@router.get("/admin",response_class=HTMLResponse)
def page_admin(request:Request,db:Session=Depends(get_db)):
    return pagina_admin(request,db)

#rota criar produto

@router.post("/admin/produto/")
async def create_produto(
    request: Request,
    nome: str = Form(...),
    preco: float = Form(...),
    quantidade: int = Form(...),
    categoria: str = Form(""),
    imagem: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    return await criar_produto(request, nome, preco, quantidade, categoria, imagem, db)
#deletar produto
@router.post("/admin/produto/deletar/{id}")
def delete_produto(id:int,db:Session=Depends(get_db)):
    return deletar_produto(id,db)



################################################################################################
#Exibir categorias

@router.get("/admin/categorias/")
def get_categorias(db:Session=Depends(get_db)):
    categorias = listar_categorias(db)
    return categorias

@router.get("/admin/categoria/{id_categoria}/produtos")
def get_produtos_categoria(id_categoria: int, db: Session = Depends(get_db)):
    produtos = listar_produtos_categoria(db, id_categoria)
    return produtos

@router.get("/admin/categoria/{id_categoria}/nome")
def get_nome_categoria(id_categoria: int, db: Session = Depends(get_db)):
    produtos = listar_nome_categoria(db, id_categoria)
    return produtos