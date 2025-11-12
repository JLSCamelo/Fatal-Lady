from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.database import get_db
from app.controllers.excluir_conta_controller import exlcuir_conta

router = APIRouter(prefix="/excluir", tags=["Usuários"])

@router.delete("/conta")
def delete_account(request: Request, db: Session = Depends(get_db)):
    return exlcuir_conta(request, db)