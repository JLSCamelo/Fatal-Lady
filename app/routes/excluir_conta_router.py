from fastapi import APIRouter, Depends, Request, Form
from sqlalchemy.orm import Session

from app.database import get_db
from app.controllers.excluir_conta_controller import (
    solicitar_exclusao_conta_controller,
    confirmar_exclusao_get_controller,
    confirmar_exclusao_post_controller,
)

router = APIRouter(prefix="/excluir", tags=["Exclusão"])


@router.post("/conta")
async def solicitar_exclusao(
    request: Request,
    db: Session = Depends(get_db),
):
    return await solicitar_exclusao_conta_controller(request, db)


@router.get("/confirmar/{token}")
def confirmar_exclusao_get(
    request: Request,
    token: str,
):
    return confirmar_exclusao_get_controller(request, token)


@router.post("/confirmar/{token}")
def confirmar_exclusao_post(
    token: str,
    cpf: str = Form(...),
    data_nascimento: str = Form(...),
    senha: str = Form(...),
    db: Session = Depends(get_db),
):
    return confirmar_exclusao_post_controller(
        token=token,
        cpf=cpf,
        data_nascimento=data_nascimento,
        senha=senha,
        db=db,
    )
