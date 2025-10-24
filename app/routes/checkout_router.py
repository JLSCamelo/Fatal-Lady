from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from database import *
from auth import *
from fastapi.templating import Jinja2Templates


router = APIRouter()
templates = Jinja2Templates(directory="views/templates")

@router.post("/checkout")
def checkout(request:Request,db:Session=Depends(get_db)):
    return checkout(request,db)

