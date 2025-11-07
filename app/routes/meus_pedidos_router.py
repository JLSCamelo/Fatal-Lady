from fastapi import APIRouter, Request, Depends
from auth import *
from controllers.meus_pedidos_controller import pedidos_usuario
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
from database import *

router = APIRouter()

@router.get("me/meus-pedidos",response_class=HTMLResponse)
def meus_pedidos(request:Request,db:Session=Depends(get_db)):
    return pedidos_usuario(request, db)
