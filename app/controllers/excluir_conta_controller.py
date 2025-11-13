from fastapi.responses import RedirectResponse
from fastapi import HTTPException, Request, Depends
from app.auth import verificar_token
from app.database import get_db
from app.models.usuario_model import UsuarioDB
from sqlalchemy.orm import Session
