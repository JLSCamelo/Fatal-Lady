from fastapi import APIRouter, Request
from datetime import datetime
from app.database import *
from app.models.usuario_model import UsuarioDB
import jwt
from app.auth import *

router = APIRouter()


@router.middleware("http")
async def atualizar_atividade(request: Request, call_next):
    response = await call_next(request)

    # precisa estar logado
    token = request.cookies.get("token")
    if token:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub_id")

        if user_id:
            db = SessionLocal()
            user = db.query(UsuarioDB).filter(UsuarioDB.id_cliente == user_id).first()
            if user:
                user.ultima_atividade = datetime.utcnow()
                db.commit()
            db.close()

    return response
