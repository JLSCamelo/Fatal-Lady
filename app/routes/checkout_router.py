from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from app.database import *
from app.auth import *
from app.controllers.checkout_controller import checkout
from fastapi.templating import Jinja2Templates


router = APIRouter()
templates = Jinja2Templates(directory="app/views/templates")

@router.post("/checkout")
def Finalizar(request:Request,db:Session=Depends(get_db)):
    return checkout(request,db)

