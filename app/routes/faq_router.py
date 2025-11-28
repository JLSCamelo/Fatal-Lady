from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/views/templates")

@router.get("/faq", response_class=HTMLResponse)
def page_duvidas_frequentes(request: Request):
    return templates.TemplateResponse(
        "duvidasfreq.html",
        {"request": request}
    )
