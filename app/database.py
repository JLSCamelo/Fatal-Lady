from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

#postgres → é o usuário padrão do banco do Supabase.
#{PASSWORD} → o Python insere o valor da variável.
#aws-1-sa-east-1.pooler.supabase.com → é o host mostrado no painel.
#6543 → é a porta do connection pooler.
#postgres → é o nome padrão do banco.

# Dados do Supabase
USER = "postgres.xomisypdbkawfgzsddwn"
PASSWORD = "fatallady"
HOST = "aws-1-sa-east-1.pooler.supabase.com"
PORT = 6543
DBNAME = "postgres"

# URL de conexão com PostgreSQL (Supabase)
DATABASE_URL =  (
    f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}"  
)

# Criar o engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # evita perda de conexão
)

# Criar sessões
SessionLocal = sessionmaker(bind=engine)

# Base para os models
Base = declarative_base()

# Dependência para injetar sessão (FastAPI)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

"""
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


DATABASE_URL = "sqlite:///./produtos.db"

engine = create_engine(DATABASE_URL, connect_args={
    "check_same_thread":False
})

# Criar sessões
SessionLocal = sessionmaker(bind=engine)

# Base para os models
Base = declarative_base()

#AJUSTES
#função para Dependência para injetar sessão no FastAPI
def get_db():
    db = SessionLocal()
    try:yield db
    finally:db.close()
"""