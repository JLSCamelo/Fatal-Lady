from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


DATABASE_URL = "mysql+pymysql://BackEnd:devback@localhost:3306/faltallady_bd"

engine = create_engine(DATABASE_URL)

# Criar sessões
SessionLocal = sessionmaker(autocommit=False, bind=engine)

# Base para os models
Base = declarative_base()


#AJUSTES



