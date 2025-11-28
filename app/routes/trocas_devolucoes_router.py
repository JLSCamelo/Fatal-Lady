from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/views/templates")

@router.get("/politicas/trocas/devolucoes", response_class=HTMLResponse)
def page_trocas_devolucoes(request: Request):
    return templates.TemplateResponse(
        "trocas_devolucoes.html",
        {"request": request}
    )
