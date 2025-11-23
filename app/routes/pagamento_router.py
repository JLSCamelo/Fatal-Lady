from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import datetime

from app.database import get_db
from app.auth import verificar_token
from app.models.usuario_model import UsuarioDB
from app.models.pedido_model import PedidoDB
from app.models.pagamento_model import PagamentoDB
from app.controllers.pagamento_controller import criar_pagamento, atualizar_status
from datetime import datetime, timedelta


router = APIRouter(prefix="/pagamentos")
templates = Jinja2Templates(directory="app/views/templates")

PIX_CHAVE = "8504417b-c306-44b8-8064-bef638fade7f"

def _get_usuario_e_pedido(request: Request, db: Session, pedido_id: int):
    token = request.cookies.get("token")
    payload = verificar_token(token)

    if not payload:
        return None, None, RedirectResponse(url="/login", status_code=303)

    email = payload.get("sub")
    usuario = db.query(UsuarioDB).filter_by(email=email).first()

    if not usuario:
        return None, None, RedirectResponse(url="/login", status_code=303)

    pedido = (
        db.query(PedidoDB)
        .filter_by(id=pedido_id, id_cliente=usuario.id_cliente)
        .first()
    )

    if not pedido:
        # se o pedido não encontrado ou não pertence ao usuário ele retorna ao carrinho
        return usuario, None, RedirectResponse(url="/carrinho", status_code=303)

    return usuario, pedido, None


# -------------------------------
# PÁGINA PRINCIPAL DE PAGAMENTOS
# -------------------------------

# aqui ele exibe tanto os dados e o id do pedido quanto permite o usuario escolher o pagamento
@router.get("/", response_class=HTMLResponse)
def pagina_pagamentos(
    request: Request,
    pedido_id: int,
    db: Session = Depends(get_db),
):
    usuario, pedido, redirect = _get_usuario_e_pedido(request, db, pedido_id)
    if redirect:
        return redirect

    pagamento = db.query(PagamentoDB).filter_by(pedido_id=pedido.id).first()

    context = {
        "request": request,
        "usuario": usuario,
        "pedido": pedido,
        "pagamento": pagamento,
        "pagamento_selecionado": pagamento.tipo_pagamento if pagamento else None,
    }
    return templates.TemplateResponse("pagamentos.html", context)


# -------------------------------
# CARTÃO DE CRÉDITO
# -------------------------------

@router.get("/cartao-credito", response_class=HTMLResponse)
def pagina_pagamento_cartao(
    request: Request,
    pedido_id: int,
    db: Session = Depends(get_db),
):
    """
    Mostra a mesma página de pagamentos, já com o tipo 'cartao_credito' selecionado.
    """
    usuario, pedido, redirect = _get_usuario_e_pedido(request, db, pedido_id)
    if redirect:
        return redirect

    pagamento = db.query(PagamentoDB).filter_by(pedido_id=pedido.id).first()

    context = {
        "request": request,
        "usuario": usuario,
        "pedido": pedido,
        "pagamento": pagamento,
        "tipo_pagamento_selecionado": "cartao_credito",
    }
    return templates.TemplateResponse("pagamentos.html", context)


@router.post("/cartao-credito")
def processar_pagamento_cartao_credito(
    request: Request,
    pedido_id: int = Form(...),
    numero_cartao: str = Form(...),
    nome_titular: str = Form(...),
    validade: str = Form(...),
    cvv: str = Form(...),
    parcelas: int = Form(1),
    bandeira: str = Form(None),
    db: Session = Depends(get_db),
):
    """
    processar o formulário de cartão de crédito.
    cria/atualiza PagamentoDB do pedido
    salva últimos 4 dígitos, bandeira e parcelas
    redireciona para /me/meus-pedidos
    """
    usuario, pedido, redirect = _get_usuario_e_pedido(request, db, pedido_id)
    if redirect:
        return redirect

    # cria o registro de pagamento
    pagamento = db.query(PagamentoDB).filter_by(pedido_id=pedido.id).first()
    if not pagamento:
        pagamento = criar_pagamento(db, pedido.id, "cartao_credito", pedido.valortotal)

    # atualiza no bd informações específicas do cartão
    pagamento.tipo_pagamento = "cartao_credito"
    pagamento.metodo_pagamento = pagamento.metodo_pagamento or "manual"
    pagamento.ultimos_digitos_cartao = numero_cartao[-4:]
    pagamento.bandeira_cartao = bandeira or pagamento.bandeira_cartao
    pagamento.parcelas = parcelas
    pagamento.data_atualizacao = datetime.utcnow()

    db.add(pagamento)
    db.commit()
    db.refresh(pagamento)


    atualizar_status(db, pagamento.id, "pago")
    return RedirectResponse(url="/me/meus-pedidos", status_code=303)





# CARTÃO DE DÉBITO ---------------------------------------------

@router.get("/cartao-debito", response_class=HTMLResponse)
def pagina_pagamento_cartao_debito(
    request: Request,
    pedido_id: int,
    db: Session = Depends(get_db),
):
    usuario, pedido, redirect = _get_usuario_e_pedido(request, db, pedido_id)
    if redirect:
        return redirect

    pagamento = db.query(PagamentoDB).filter_by(pedido_id=pedido.id).first()

    context = {
        "request": request,
        "usuario": usuario,
        "pedido": pedido,
        "pagamento": pagamento,
        "tipo_pagamento_selecionado": "cartao_debito",
    }
    return templates.TemplateResponse("pagamentos.html", context)


@router.post("/cartao-credito")
def processar_pagamento_cartao(
    request: Request,
    pedido_id: int = Form(...),
    numero_cartao: str = Form(...),
    nome_titular: str = Form(...),
    validade: str = Form(...),
    cvv: str = Form(...),
    bandeira: str = Form(None),
    db: Session = Depends(get_db),
):
    """
    processar o formulário de cartão de débito.
    cria/atualiza PagamentoDB do pedido
    salva últimos 4 dígitos e bandeira, mas não há as parcelas (nao sei se pode conflitar no banco por isso)
    redireciona para /me/meus-pedidos
    """
    usuario, pedido, redirect = _get_usuario_e_pedido(request, db, pedido_id)
    if redirect:
        return redirect

    # cria o registro de pagamento
    pagamento = db.query(PagamentoDB).filter_by(pedido_id=pedido.id).first()
    if not pagamento:
        pagamento = criar_pagamento(db, pedido.id, "cartao_credito", pedido.valortotal)

    # atualiza no bd informações específicas do cartão
    pagamento.tipo_pagamento = "cartao_credito"
    pagamento.metodo_pagamento = pagamento.metodo_pagamento or "manual"
    pagamento.ultimos_digitos_cartao = numero_cartao[-4:]
    pagamento.bandeira_cartao = bandeira or pagamento.bandeira_cartao
    pagamento.data_atualizacao = datetime.utcnow()

    db.add(pagamento)
    db.commit()
    db.refresh(pagamento)


    atualizar_status(db, pagamento.id, "pago")
    return RedirectResponse(url="/me/meus-pedidos", status_code=303)





# PAGAMENTO POR PIX -------------------------------------

@router.get("/pix", response_class=HTMLResponse)
def pagina_pagamento_pix(
    request: Request,
    pedido_id: int,
    db: Session = Depends(get_db),
):
    """
    tempo limite de expiração de 10 minutos (somente no front sem relação com o banco)
    garante que exista a relação com o pagamentoDB com tipo 'pix' para o pedido
    o certo seria justamente ter xconexão com o gateway do banco para q a cada 10 minutos mude o QR Code,
    no entanto, foi feita apenas uma simulação visual (utilizei ajuda do chatgpt para melhor efetuação do pagamento)
    """
    usuario, pedido, redirect = _get_usuario_e_pedido(request, db, pedido_id)
    if redirect:
        return redirect

    pagamento = db.query(PagamentoDB).filter_by(pedido_id=pedido.id).first()
    if not pagamento:
        pagamento = criar_pagamento(db, pedido.id, "pix", pedido.valortotal)

    # Configura o pagamento como PIX com a chave fixa
    pagamento.tipo_pagamento = "pix"
    pagamento.metodo_pagamento = pagamento.metodo_pagamento or "pix"
    pagamento.codigo_pix = PIX_CHAVE
    pagamento.data_atualizacao = datetime.utcnow()

    db.add(pagamento)
    db.commit()
    db.refresh(pagamento)

    # expiração em 10 minutos - NAO MUDAR O TEMPO!!!!! 😓
    # FUNCIONA SOMENTE NO FRONT para nao ter que mexer no banco de dados
    expiracao = datetime.utcnow() + timedelta(minutes=10)
    expiracao_ts_ms = int(expiracao.timestamp() * 1000)

    context = {
        "request": request,
        "usuario": usuario,
        "pedido": pedido,
        "pagamento": pagamento,
        "tipo_pagamento_selecionado": "pix",
        "pix_chave": PIX_CHAVE,
        "pix_expiracao_ts": expiracao_ts_ms,
    }
    return templates.TemplateResponse("pagamentos.html", context)


@router.post("/pix/confirmar")
def confirmar_pagamento_pix(
    request: Request,
    pedido_id: int = Form(...),
    db: Session = Depends(get_db),
):
    """
    Usuário clicou em 'Já paguei / Enviar'.
    Aqui você poderia integrar com o banco/gateway para confirmar,
    mas por enquanto só manda para Meus Pedidos.
    """
    usuario, pedido, redirect = _get_usuario_e_pedido(request, db, pedido_id)
    if redirect:
        return redirect

    pagamento = db.query(PagamentoDB).filter_by(pedido_id=pedido.id).first()
    if not pagamento:
        # fallback defensivo: cria de novo se não existir
        pagamento = criar_pagamento(db, pedido.id, "pix", pedido.valortotal)
        pagamento.tipo_pagamento = "pix"
        pagamento.metodo_pagamento = pagamento.metodo_pagamento or "pix"
        pagamento.codigo_pix = PIX_CHAVE
        db.add(pagamento)
        db.commit()

    atualizar_status(db, pagamento.id, "pago")

    return RedirectResponse(url="/me/meus-pedidos", status_code=303)



# BOLETO -------------------------------

@router.get("/boleto", response_class=HTMLResponse)
def pagina_pagamento_boleto(
    request: Request,
    pedido_id: int,
    db: Session = Depends(get_db),
):
    usuario, pedido, redirect = _get_usuario_e_pedido(request, db, pedido_id)
    if redirect:
        return redirect

    pagamento = db.query(PagamentoDB).filter_by(pedido_id=pedido.id).first()

    context = {
        "request": request,
        "usuario": usuario,
        "pedido": pedido,
        "pagamento": pagamento,
        "tipo_pagamento_selecionado": "boleto",
    }
    return templates.TemplateResponse("pagamentos.html", context)


@router.post("/boleto")
def processar_pagamento_boleto(
    request: Request,
    pedido_id: int = Form(...),
    codigo_barras: str = Form(...),
    db: Session = Depends(get_db),
):
    """
    para falar a verdade estes campos nao deveriam ser para forms, uma vez que em sites a propria empresa
    gera um boleto para a gente. logo, teoricamente deveria existir um codigo de barras propriamente do
    Fatal Lady, mas para a conformidade com o banco de dados esta temporariamente assim
    """
    usuario, pedido, redirect = _get_usuario_e_pedido(request, db, pedido_id)
    if redirect:
        return redirect

    pagamento = db.query(PagamentoDB).filter_by(pedido_id=pedido.id).first()
    if not pagamento:
        pagamento = criar_pagamento(db, pedido.id, "boleto", pedido.valortotal)

    pagamento.tipo_pagamento = "boleto"
    pagamento.metodo_pagamento = pagamento.metodo_pagamento or "manual"
    pagamento.codigo_barras = codigo_barras
    pagamento.data_atualizacao = datetime.utcnow()

    db.add(pagamento)
    db.commit()
    db.refresh(pagamento)

    atualizar_status(db, pagamento.id, "pago")

    return RedirectResponse(url="/me/meus-pedidos", status_code=303)
