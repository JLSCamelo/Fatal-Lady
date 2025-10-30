from fastapi import Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from datetime import datetime

from auth import verificar_token
from models.usuario_model import UsuarioDB
from models.carrinho_model import CarrinhoDB, ItemCarrinhoDB
from models.pedido_model import PedidoDB, ItemPedidoDB  

def checkout(request: Request, db: Session):
    token = request.cookies.get("token")
    payload = verificar_token(token)
    if not payload:
        return RedirectResponse(url="/login", status_code=303)

    email = payload.get("sub")
    usuario = db.query(UsuarioDB).filter_by(email=email).first()

    # Busca o carrinho atual
    carrinho = db.query(CarrinhoDB).filter_by(id_cliente=usuario.id_cliente).first()
    if not carrinho:
        return {"mensagem": "Carrinho vazio"}

    itens_carrinho = db.query(ItemCarrinhoDB).filter_by(carrinho_id=carrinho.id).all()
    if not itens_carrinho:
        return {"mensagem": "Nenhum item no carrinho"}

    # Calcula o total
    total = sum(item.quantidade * item.preco_unitario for item in itens_carrinho)

    # Cria o pedido
    pedido = PedidoDB(
        id_cliente=usuario.id_cliente,
        data=datetime.utcnow(),
        valortotal=total,
        status="Em processamento"  # se houver campo status
    )
    db.add(pedido)
    db.commit()
    db.refresh(pedido)

    # Cria os itens do pedido
    for item in itens_carrinho:
        item_pedido = ItemPedidoDB(
            pedido_id=pedido.id,       # FK para PedidoDB
            produto_id=item.produto_id,       # FK para ProdutoDB
            quantidade=item.quantidade,
            preco_unitario=item.preco_unitario
        )
        db.add(item_pedido)

    db.commit()

    # (Opcional) limpa o carrinho
    db.query(ItemCarrinhoDB).filter_by(carrinho_id=carrinho.id).delete()
    carrinho.valortotal = 0
    db.commit()

    return RedirectResponse(url="/meus-pedidos", status_code=303)
