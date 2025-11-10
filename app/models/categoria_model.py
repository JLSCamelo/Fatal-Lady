from sqlalchemy import Column, Integer, String
from app.database import * 
# import sql puro para add uma nova coluna
# from sqlalchemy import text
from app.models.usuario_model import UsuarioDB
from sqlalchemy.orm import relationship


#tabela Categoria
class CategoriaDB(Base):
    __tablename__ = "categoria"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String) 
    descricao = Column(String, nullable=True)

     # Relacionamento com produtos
    produtos = relationship("ProdutoDB", back_populates="categoria")
