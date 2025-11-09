from sqlalchemy import Column, Integer, String, ForeignKey
from database import *
# from sqlalchemy import text
from sqlalchemy.orm import relationship
from models.usuario_model import UsuarioDB

class EnderecoDB(Base):
    __tablename__ = "enderecos"

    id_endereco = Column(Integer, primary_key=True, index=True)
    id_cliente= Column(Integer, ForeignKey("usuarios.id_cliente"), nullable=False)

    cep = Column(String, nullable=True)     
    rua = Column(String, nullable=True)
    numero = Column(String, nullable=True)
    cidade = Column(String, nullable=True)
    complemento = Column(String, nullable=True)
    
    # Relacionamento com usuário
    usuario = relationship("UsuarioDB", back_populates="enderecos")

