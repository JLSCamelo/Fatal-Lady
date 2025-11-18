# NAO FUNCIONANDO!!!!!!!!!!!!!!!!!!!!!!!!!! por enquanto
from fastapi import APIRouter, Request, Depends, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.controllers.pagamento_controller import criar_pagamento, atualizar_status
from app.models.pagamento_model import PagamentoDB
from datetime import datetime
import json

router = APIRouter()
templates = Jinja2Templates(directory="app/views/templates")

@router.get("/pagamentos")
def pagamentos_page(request: Request, pedido_id: int, db: Session = Depends(get_db)):
    # mostra opções de pagamento para o pedido
    return templates.TemplateResponse("payments/options.html", {"request": request, "pedido_id": pedido_id})

@router.post("/pagamentos/iniciar")
async def iniciar_pagamento(
    request: Request,
    pedido_id: int = Form(...),
    metodo: str = Form(...),
    valor: float = Form(...),
    db: Session = Depends(get_db)
):
    # método de pagamento
    metodo = metodo.lower()

    if metodo == "boleto":
        tipo_pagamento = "boleto"
    elif metodo == "pix":
        tipo_pagamento = "pix"
    elif metodo == "cartao":
        tipo_pagamento = "cartao_credito"
    elif metodo == "debito":
        tipo_pagamento = "cartao_debito"
    elif metodo == "transferencia":
        tipo_pagamento = "transferencia"
    else:
        tipo_pagamento = "boleto"


    # cria pagamento
    pagamento = criar_pagamento(
        db = db, 
        pedido_id = pedido_id, 
        tipo_pagamento=tipo_pagamento,
        valor_total=valor
    )

    # redirecionamento por método
    if metodo == "boleto":
        return RedirectResponse(f"/pagamentos/boleto?pagamento_id={pagamento.id}", status_code=303)

    if metodo == "pix":
        return RedirectResponse(f"/pagamentos/pix?pagamento_id={pagamento.id}", status_code=303)

    if metodo in ("cartao", "debito"):
        return RedirectResponse(f"/pagamentos/cartao?pagamento_id={pagamento.id}", status_code=303)

    if metodo == "transferencia":
        return RedirectResponse(f"/pagamentos/transferencia?pagamento_id={pagamento.id}", status_code=303)

    return RedirectResponse("/", status_code=303)

# página de status
@router.get("/pagamentos/success")
def pagamento_success(request: Request):
    return templates.TemplateResponse("payments/success.html", {"request": request})

@router.get("/pagamentos/cancel")
def pagamento_cancel(request: Request):
    return templates.TemplateResponse("payments/cancel.html", {"request": request})

# páginas simples para cada método
@router.get("/pagamentos/boleto")
def pagamento_boleto(request: Request, pagamento_id: int, db: Session = Depends(get_db)):
    pagamento = db.query(PagamentoDB).filter_by(id=pagamento_id).first()
    return templates.TemplateResponse("payments/boleto.html", {"request": request, "pagamento": pagamento})


@router.get("/pagamentos/pix")
def pagamento_pix(request: Request, pagamento_id: int, db: Session = Depends(get_db)):
    pagamento = db.query(PagamentoDB).filter_by(id=pagamento_id).first()

    codigo_pix = f"PIX-{pagamento.id}-{pagamento.pedido_id}"

    return templates.TemplateResponse(
        "payments/pix.html",
        {"request": request, "pagamento": pagamento, "codigo_pix": codigo_pix}
    )


@router.get("/pagamentos/cartao")
def pagamento_cartao(request: Request, pagamento_id: int, db: Session = Depends(get_db)):
    pagamento = db.query(PagamentoDB).filter_by(id=pagamento_id).first()
    return templates.TemplateResponse("payments/cartao.html", {"request": request, "pagamento": pagamento})


# ===============================
# PROCESSAR PAGAMENTO COM CARTÃO
# ===============================
@router.post("/pagamentos/cartao/processar")
def processar_cartao(
    request: Request,
    pagamento_id: int = Form(...),
    numero: str = Form(...),
    validade: str = Form(...),
    cvv: str = Form(...),
    nome: str = Form(...),
    db: Session = Depends(get_db)
):
    pagamento = db.query(PagamentoDB).filter_by(id=pagamento_id).first()
    if not pagamento:
        return {"error": "pagamento nao encontrado"}

    atualizar_status(db, pagamento.id, "aprovado")

    # atualizar pedido
    pedido = pagamento.pedido
    if pedido:
        pedido.status = "pago"
        db.add(pedido)
        db.commit()

    return RedirectResponse(url="/pagamentos/success", status_code=303)


# ===============================
# TRANSFERÊNCIA BANCÁRIA
# ===============================
@router.get("/pagamentos/transferencia")
def pagamento_transferencia(request: Request, pagamento_id: int, db: Session = Depends(get_db)):
    pagamento = db.query(PagamentoDB).filter_by(id=pagamento_id).first()

    dados_banco = {
        "banco": "001 - Banco do Brasil",
        "agencia": "0001",
        "conta": "123456-7",
        "favorecido": "Fatal Lady LTDA"
    }

    return templates.TemplateResponse(
        "payments/transferencia.html",
        {"request": request, "pagamento": pagamento, "dados_banco": dados_banco}
    )