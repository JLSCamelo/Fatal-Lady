# NAO FUNCIONANDO!!!!!!!!!!!!!!!!!!!!!!!!!! por enquanto
from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from app.models.pagamento_model import PagamentoDB, StatusPagamento, TipoPagamento, HistoricoPagamentoDB

def criar_pagamento(db: Session, pedido_id: int, tipo: TipoPagamento, dados: dict):
    """
    Cria um pagamento interno no banco sem usar gateway externo.
    tipo: TipoPagamento (BOLETO, PIX, CARTAO, DEBITO, TRANSFERENCIA)
    dados: dicionario com metadados conforme tipo (ex: cpf, banco, agencia, etc.)
    """
    pagamento = PagamentoDB(
        pedido_id=pedido_id,
        valor=dados.get("valor"),
        tipo=tipo.value if hasattr(tipo, 'value') else str(tipo),
        status=StatusPagamento.PENDENTE.value,
        dados=dados.get("dados_json") if dados else None,
        data_criacao=datetime.utcnow()
    )
    db.add(pagamento)
    db.commit()
    db.refresh(pagamento)

    # cria histórico inicial
    historico = HistoricoPagamentoDB(
        pagamento_id=pagamento.id,
        status=StatusPagamento.PENDENTE,
        mensagem="Pagamento criado no sistema"
    )
    db.add(historico)
    db.commit()

    return pagamento

def atualizar_status(db: Session, pagamento_id: int, novo_status: StatusPagamento, mensagem: str = None):
    pagamento = db.query(PagamentoDB).filter(PagamentoDB.id == pagamento_id).first()
    if not pagamento:
        raise HTTPException(status_code=404, detail="Pagamento não encontrado")
    pagamento.status = novo_status.value if hasattr(novo_status, 'value') else str(novo_status)
    db.add(pagamento)
    # criar historico
    historico = HistoricoPagamentoDB(
        pagamento_id=pagamento.id,
        status=novo_status,
        mensagem=mensagem
    )
    db.add(historico)
    db.commit()
    db.refresh(pagamento)
    return pagamento
