from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class EnderecoDB(Base):
    __tablename__ = "enderecos"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id_cliente"))
    cep = Column(String(10), nullable=False)
    rua = Column(String(120), nullable=False)
    bairro = Column(String(120), nullable=False)
    cidade = Column(String(120), nullable=False)
    estado = Column(String(2), nullable=False)
    complemento = Column(String(120))
    numero = Column(String, nullable=False )

    usuario = relationship("UsuarioDB", back_populates="enderecos")
