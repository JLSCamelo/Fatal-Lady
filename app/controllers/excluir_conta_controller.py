from fastapi import HTTPException, Request, Depends
from app.auth import verificar_token
from app.database import get_db
from app.models.usuario_model import UsuarioDB
from sqlalchemy.orm import Session

def exlcuir_conta(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("token")
    if not token:
        raise HTTPException(status_code=401, detail="Usuário não autenticado")

    payload = verificar_token(token)
    email = payload.get("sub")

    usuario = db.query(UsuarioDB).filter(UsuarioDB.email == email).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    db.delete(usuario)
    db.commit()
    return {"message": "Conta excluída com sucesso"}