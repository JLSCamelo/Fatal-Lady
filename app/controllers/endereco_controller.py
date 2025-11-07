from fastapi import Form, Request, File
from fastapi.responses import RedirectResponse
import os, shutil
from database import *
from models.usuario_model import UsuarioDB
from fastapi.templating import Jinja2Templates
from auth import *
from sqlalchemy.orm import Session

templates =Jinja2Templates(directory="views/templates")




