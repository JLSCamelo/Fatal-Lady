from sqlalchemy import Column, Integer, String
from database import *

class FabricanteDB(Base):
    __tablename__ = "fabricantes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    cidade = Column(String, nullable=True)
    pais = Column(String, nullable=True)
    estado = Column(String, nullable=True)
