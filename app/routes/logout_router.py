from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from controllers.logout_controler import *


router = APIRouter()
templates = Jinja2Templates(directory="views/templates")

# Logout
@router.get("/logout")
def logout(request: Request):
    return logout_controller(request)
