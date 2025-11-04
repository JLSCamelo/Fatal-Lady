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
        status="Em processamento"
    )
    db.add(pedido)
    db.commit()
    db.refresh(pedido)

    # Cria os itens do pedido
    for item in itens_carrinho:
        item_pedido = ItemPedidoDB(
            pedido_id=pedido.id,
            produto_id=item.produto_id,
            quantidade=item.quantidade,
            preco_unitario=item.preco_unitario
        )
        db.add(item_pedido)

    db.commit()

        # Antes de remover os itens do carrinho, salve os dados que serão usados
    itens_email = []
    for item in itens_carrinho:
        produto_nome = getattr(item, "nome_produto", f"Produto {item.produto_id}")
        itens_email.append({
            "nome": produto_nome,
            "quantidade": item.quantidade,
            "preco": item.preco_unitario
        })

    # Agora pode deletar os itens do carrinho
    for item in itens_carrinho:
        db.delete(item)
    db.commit()

    # Depois envie o e-mail usando a lista que você salvou
    enviar_email_checkout(
        destinatario=usuario.email,
        nome_usuario=usuario.nome,
        itens=itens_email,
        total=total
    )


    # Redireciona para a página de pedidos
    return RedirectResponse(url="/meus-pedidos", status_code=303)



import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv

load_dotenv()
EMAIL_REMITENTE = os.getenv("EMAIL_REMITENTE")
EMAIL_SENHA = os.getenv("EMAIL_SENHA")
EMAIL_FROM_NAME = os.getenv("EMAIL_FROM_NAME", EMAIL_REMITENTE)


def enviar_email_checkout(destinatario: str, nome_usuario: str, itens: list, total: float):
    """
    Envia um e-mail HTML personalizado com o resumo do pedido.
    :param destinatario: e-mail do cliente
    :param nome_usuario: nome do cliente
    :param itens: lista de dicionários [{'nome': 'Sandália X', 'quantidade': 2, 'preco': 129.9}, ...]
    :param total: valor total do pedido
    """
    if not EMAIL_REMITENTE or not EMAIL_SENHA:
        raise RuntimeError("Configurações de e-mail não definidas. Verifique o .env")

    msg = EmailMessage()
    msg["Subject"] = "🛍️ Seu pedido na Fatal Lady foi confirmado!"
    msg["From"] = EMAIL_FROM_NAME
    msg["To"] = destinatario

    # Gera tabela de produtos
    linhas_itens = ""
    for item in itens:
        subtotal = item["quantidade"] * item["preco"]
        linhas_itens += f"""
        <tr>
            <td style="padding:8px 12px; border:1px solid #ddd;">{item['nome']}</td>
            <td style="padding:8px 12px; border:1px solid #ddd; text-align:center;">{item['quantidade']}</td>
            <td style="padding:8px 12px; border:1px solid #ddd; text-align:right;">R$ {item['preco']:.2f}</td>
            <td style="padding:8px 12px; border:1px solid #ddd; text-align:right;">R$ {subtotal:.2f}</td>
        </tr>
        """

    html_content = f"""
    <html>
      <body style="font-family:'Poppins',Arial,sans-serif; background-color:#f9f9f9; padding:20px;">
        <table width="100%" cellpadding="0" cellspacing="0" style="max-width:600px; margin:auto; background:#fff; border-radius:10px; overflow:hidden;">
          <tr>
            <td align="center" style="padding:30px 0;">
              <h1 style="color:#000; font-size:26px;">FATAL <span style="color:#d00000;">LADY</span></h1>
              <p>Olá, <b>{nome_usuario}</b>! 👋</p>
              <p>Seu pedido foi <b>confirmado</b> e já está em processamento.</p>
            </td>
          </tr>

          <tr>
            <td style="padding:20px;">
              <h3>Resumo do Pedido:</h3>
              <table width="100%" cellspacing="0" cellpadding="0" style="border-collapse:collapse; margin-top:10px;">
                <thead>
                  <tr style="background-color:#f2f2f2;">
                    <th style="padding:8px 12px; border:1px solid #ddd;">Produto</th>
                    <th style="padding:8px 12px; border:1px solid #ddd;">Qtd</th>
                    <th style="padding:8px 12px; border:1px solid #ddd;">Preço</th>
                    <th style="padding:8px 12px; border:1px solid #ddd;">Subtotal</th>
                  </tr>
                </thead>
                <tbody>
                  {linhas_itens}
                </tbody>
                <tfoot>
                  <tr style="background-color:#f2f2f2;">
                    <td colspan="3" style="padding:8px 12px; border:1px solid #ddd; text-align:right;"><b>Total:</b></td>
                    <td style="padding:8px 12px; border:1px solid #ddd; text-align:right;"><b>R$ {total:.2f}</b></td>
                  </tr>
                </tfoot>
              </table>
            </td>
          </tr>

          <tr>
            <td align="center" style="padding:20px;">
              <a href="https://fatallady.com.br/meus-pedidos" style="display:inline-block; background-color:#d00000; color:#fff; padding:14px 28px; border-radius:4px; text-decoration:none; font-weight:bold;">
                Acompanhar Pedido
              </a>
            </td>
          </tr>

          <tr>
            <td align="center" style="padding:20px; background-color:#000; color:#fff; font-size:13px;">
              <p>Frete grátis em compras acima de R$299</p>
              <p>© 2025 Fatal Lady. Todos os direitos reservados.</p>
            </td>
          </tr>
        </table>
      </body>
    </html>
    """
    msg.add_alternative(html_content, subtype="html")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_REMITENTE, EMAIL_SENHA)
        smtp.send_message(msg)



# def checkout(request: Request, db: Session):
#     token = request.cookies.get("token")
#     payload = verificar_token(token)
#     if not payload:
#         return RedirectResponse(url="/login", status_code=303)

#     email = payload.get("sub")
#     usuario = db.query(UsuarioDB).filter_by(email=email).first()

#     # Busca o carrinho atual
#     carrinho = db.query(CarrinhoDB).filter_by(id_cliente=usuario.id_cliente).first()
#     if not carrinho:
#         return {"mensagem": "Carrinho vazio"}

#     itens_carrinho = db.query(ItemCarrinhoDB).filter_by(carrinho_id=carrinho.id).all()
#     if not itens_carrinho:
#         return {"mensagem": "Nenhum item no carrinho"}

#     # Calcula o total
#     total = sum(item.quantidade * item.preco_unitario for item in itens_carrinho)

#     # Cria o pedido
#     pedido = PedidoDB(
#         id_cliente=usuario.id_cliente,
#         data=datetime.utcnow(),
#         valortotal=total,
#         status="Em processamento"  # se houver campo status
#     )
#     db.add(pedido)
#     db.commit()
#     db.refresh(pedido)

#     # Cria os itens do pedido
#     for item in itens_carrinho:
#         item_pedido = ItemPedidoDB(
#             pedido_id=pedido.id,       # FK para PedidoDB
#             produto_id=item.produto_id,       # FK para ProdutoDB
#             quantidade=item.quantidade,
#             preco_unitario=item.preco_unitario
#         )
#         db.add(item_pedido)

#     db.commit()

#     db.query(ItemCarrinhoDB).filter_by(carrinho_id=carrinho.id).delete()
#     carrinho.valortotal = 0
#     db.commit()

#     return RedirectResponse(url="/meus-pedidos", status_code=303)

