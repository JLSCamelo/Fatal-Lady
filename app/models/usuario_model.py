from sqlalchemy import Column, Integer, String, Boolean
from database import *
from sqlalchemy import text

# from sqlalchemy.orm import relationship
# from models.produto_model import ProdutoDB

class UsuarioDB(Base):
    __tablename__ = "usuarios"

    id_cliente = Column(Integer,primary_key=True,index=True)
    nome = Column(String,nullable=False,index=True)
    email = Column(String, nullable=False, unique=True)
    senha = Column(String(200),nullable=False) 
    cep = Column(Integer,nullable=False)
    rua = Column(String,nullable=True)
    cidade = Column(String,nullable=False)
    telefone = Column(String,nullable=True)
    is_admin=Column(Boolean, default=False)
    

#criar banco e tabelas
Base.metadata.create_all(bind=engine)
