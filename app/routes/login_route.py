from fastapi import APIRouter, Request, Form, UploadFile, File, Depends 
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import HTTPException
from fastapi.templating import Jinja2Templates
import os, shutil
from sqlalchemy.orm import Session
from database import get_db
from controllers.controller_login import *
from auth import *

router = APIRouter() #rotas
templates = Jinja2Templates(directory="views/templates") #front-end

#login usuario
router.get("/login",response_class=HTMLResponse)
def home(request:Request):
    return templates.TemplateResponse("login.html",{
        "request":request
    })

#cadastro do login
@router.post("/login")
def login(request: Request,
          email: str = Form(...),
          senha: str = Form(...),
          db: Session = Depends(get_db)):
    return login_controller(request, email, senha, db)

# pagina do usuario
@router.get("/dashboard", response_class=HTMLResponse)
def dashboard(request:Request):
    token=request.cookies.get("token")
    if not token or not verificar_token(token):
        return RedirectResponse(url="/", status_code=303)
    return templates.TemplateResponse("index.html",
                                      {"request":request})
