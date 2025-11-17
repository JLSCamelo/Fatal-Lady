# NAO FUNCIONANDO!!!!!!!!!!!!!!!!!!!!!!!!!! por enquanto
from fastapi import APIRouter, Request, Depends, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.controllers.pagamento_controller import criar_pagamento, atualizar_status
from app.models.pagamento_model import TipoPagamento, StatusPagamento
import json

router = APIRouter()
templates = Jinja2Templates(directory="app/views/templates")

@router.get("/pagamentos")
def pagamentos_page(request: Request, pedido_id: int, db: Session = Depends(get_db)):
    # mostra opções de pagamento para o pedido
    return templates.TemplateResponse("payments/options.html", {"request": request, "pedido_id": pedido_id})

@router.post("/pagamentos/iniciar")
def iniciar_pagamento(request: Request, pedido_id: int = Form(...), metodo: str = Form(...), db: Session = Depends(get_db)):
    # Recebe formulário com metodo do pagamento
    tipo = None
    metodo = metodo.lower()
    if metodo == "boleto":
        tipo = TipoPagamento.BOLETO
    elif metodo == "pix":
        tipo = TipoPagamento.PIX
    elif metodo == "cartao":
        tipo = TipoPagamento.CARTAO_CREDITO
    elif metodo == "debito":
        tipo = TipoPagamento.CARTAO_DEBITO
    elif metodo == "transferencia":
        tipo = TipoPagamento.TRANSFERENCIA
    else:
        tipo = TipoPagamento.BOLETO

    # valor será buscado do pedido na view/cliente ou enviado via form
    dados = {"valor": float(request.form().get("valor", 0)) if hasattr(request, "form") else 0}
    # Criar pagamento no DB
    pagamento = criar_pagamento(db, pedido_id, tipo, {"valor": dados.get("valor"), "dados_json": json.dumps({})})
    # redirecionar para página específica por método
    if metodo == "boleto":
        return RedirectResponse(url=f"/pagamentos/boleto?pagamento_id={pagamento.id}", status_code=303)
    if metodo == "pix":
        return RedirectResponse(url=f"/pagamentos/pix?pagamento_id={pagamento.id}", status_code=303)
    if metodo in ("cartao","debito"):
        return RedirectResponse(url=f"/pagamentos/cartao?pagamento_id={pagamento.id}", status_code=303)
    if metodo == "transferencia":
        return RedirectResponse(url=f"/pagamentos/transferencia?pagamento_id={pagamento.id}", status_code=303)

    return RedirectResponse(url="/", status_code=303)

@router.get("/pagamentos/success")
def pagamento_success(request: Request):
    return templates.TemplateResponse("payments/success.html", {"request": request})

@router.get("/pagamentos/cancel")
def pagamento_cancel(request: Request):
    return templates.TemplateResponse("payments/cancel.html", {"request": request})

# páginas simples para cada método
@router.get("/pagamentos/boleto")
def pagamento_boleto(request: Request, pagamento_id: int, db: Session = Depends(get_db)):
    pagamento = db.query(__import__("app.models.pagamento_model", fromlist=["PagamentoDB"]).PagamentoDB).filter_by(id=pagamento_id).first()
    return templates.TemplateResponse("payments/boleto.html", {"request": request, "pagamento": pagamento})

@router.get("/pagamentos/pix")
def pagamento_pix(request: Request, pagamento_id: int, db: Session = Depends(get_db)):
    pagamento = db.query(__import__("app.models.pagamento_model", fromlist=["PagamentoDB"]).PagamentoDB).filter_by(id=pagamento_id).first()
    # gerar qr e codigo pix (simulação)
    codigo_pix = f"PIX-{pagamento.id}-{pagamento.pedido_id}"
    return templates.TemplateResponse("payments/pix.html", {"request": request, "pagamento": pagamento, "codigo_pix": codigo_pix})

@router.get("/pagamentos/cartao")
def pagamento_cartao(request: Request, pagamento_id: int, db: Session = Depends(get_db)):
    pagamento = db.query(__import__("app.models.pagamento_model", fromlist=["PagamentoDB"]).PagamentoDB).filter_by(id=pagamento_id).first()
    return templates.TemplateResponse("payments/cartao.html", {"request": request, "pagamento": pagamento})

@router.post("/pagamentos/cartao/processar")
def processar_cartao(request: Request, pagamento_id: int = Form(...), numero: str = Form(...), validade: str = Form(...), cvv: str = Form(...), nome: str = Form(...), db: Session = Depends(get_db)):
    pagamento = db.query(__import__("app.models.pagamento_model", fromlist=["PagamentoDB"]).PagamentoDB).filter_by(id=pagamento_id).first()
    if not pagamento:
        return {"error":"pagamento nao encontrado"}
    # Simular aprovação
    atualizar_status(db, pagamento.id, StatusPagamento.APROVADO, "Pagamento por cartão aprovado (simulação)")
    # atualizar pedido também
    pedido = db.query(__import__("app.models.pedido_model", fromlist=["PedidoDB"]).PedidoDB).filter_by(id=pagamento.pedido_id).first()
    if pedido:
        pedido.status = "pago"
        db.add(pedido); db.commit()
    return RedirectResponse(url="/pagamentos/success", status_code=303)

@router.get("/pagamentos/transferencia")
def pagamento_transferencia(request: Request, pagamento_id: int, db: Session = Depends(get_db)):
    pagamento = db.query(__import__("app.models.pagamento_model", fromlist=["PagamentoDB"]).PagamentoDB).filter_by(id=pagamento_id).first()
    # detalhes bancarios para transferência (sao ficticios)
    dados_banco = {
        "banco": "001 - Banco do Brasil",
        "agencia": "0001",
        "conta": "123456-7",
        "favorecido": "Fatal Lady LTDA"
    }
    return templates.TemplateResponse("payments/transferencia.html", {"request": request, "pagamento": pagamento, "dados_banco": dados_banco})
