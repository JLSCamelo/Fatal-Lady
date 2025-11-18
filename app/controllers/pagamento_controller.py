from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from app.models.pagamento_model import PagamentoDB

def criar_pagamento(db: Session, pedido_id: int, tipo_pagamento: str, valor_total: float):

    pagamento = PagamentoDB(
      pedido_id = pedido_id,
      valor_total=valor_total, 
      tipo_pagamento= tipo_pagamento,
      metodo_pagamento = "manual",
      status = "pendente"
    )
    db.add(pagamento)
    db.commit()
    db.refresh(pagamento)

    return pagamento 

def atualizar_status(db: Session, pagamento_id: int, novo_status: str, mensagem: str = None):
    pagamento = db.query(PagamentoDB).filter(PagamentoDB.id == pagamento_id).first()

    if not pagamento:
        raise HTTPException(status_code=404, detail="Pagamento não encontrado")

    pagamento.status = novo_status
    pagamento.data_atualizacao = datetime.utcnow()

    db.add(pagamento)
    db.commit()
    db.refresh(pagamento)

    return pagamento
