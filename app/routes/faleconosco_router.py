from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/views/templates")

@router.get("/faleconosco", response_class=HTMLResponse)
def page_fale_conosco(request: Request):
    return templates.TemplateResponse(
        "faleconosco.html",
        {"request": request}
    )
