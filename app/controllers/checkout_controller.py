from fastapi import Request
from fastapi.responses import RedirectResponse 
from database import *
from models.pedido_model import *
from models.usuario_model import UsuarioDB
from auth import *
from sqlalchemy.orm import Session
from carrinho_controller import carrinhos

def checkout(request:Request,db:Session):
    token=request.cookies.get("token")
    payload=verificar_token(token)

    if not payload:
        return RedirectResponse(url="/login",status_code=303)
    
    email=payload.get("sub")
    usuario=db.query(UsuarioDB).filter_by(email=email).first()
    carrinho=carrinhos.get(usuario.id,[])

    if not carrinho:
        return {"mensagem": "Carrinho vazio"}
    
    total=sum(item["preco"]*item["quantidade"] for item in carrinho)
    pedido = PedidoDB(usuario_id=usuario.id,total=total)
    db.add(pedido)
    db.commit()
    db.refresh(pedido)

    #novo item
    for item in carrinho:
        novo_item=ItemPedidoDB(
            pedido_id=pedido.id,
            produto_id=item["id"],
            quantidade=item["quantidade"],
            preco_unitario=item["preco"]
        )
        db.add(novo_item)
    db.commit()

    #limpar o carrinho
    carrinhos[usuario.id]=[]#limpeza do carrinho
    return RedirectResponse("/",status_code=303)

