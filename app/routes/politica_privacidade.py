from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.usuario_model import UsuarioDB

router = APIRouter()
templates = Jinja2Templates(directory="app/views/templates")


@router.get("/privacy", response_class=HTMLResponse)
def privacy(request: Request, db: Session = Depends(get_db)):
    usuario = None
    return templates.TemplateResponse(
        "politicadeprivacidade.html",
        {"request": request, "usuario": usuario}
    )
