from fastapi import Request
from models.pedido_model import PedidoDB
from auth import *
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from models.usuario_model import UsuarioDB
from database import *

templates = Jinja2Templates(directory="templates")

def pedidos_usuario(request:Request,db:Session):
    token=request.cookies.get("token")
    payload=verificar_token(token)

    if not payload:
        return RedirectResponse(url="/login",status_code=303)
    
    email=payload.get("sub")
    usuario=db.query(UsuarioDB).filter_by(email=email).first()
    pedidos=db.query(PedidoDB).filter_by(usuario_id=usuario.id).all()

    return templates.TemplateResponse("meus_pedidos.html",
            {"request":request,"pedidos":pedidos})
