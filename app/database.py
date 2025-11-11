from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

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
    pool_pre_ping=True, 
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
# #criar banco e tabelas
# # Base.metadata.create_all(bind=engine)



"""
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from supabase import create_client, Client

# --- Parte 1: Cliente Supabase (Para Auth, Storage, etc.) ---
# Isso é para os serviços do Supabase, não para o SQLAlchemy.
supabase_api_url = "https://xomisypdbkawfgzsddwn.supabase.co"
supabase_api_key = "sua_anon_key_aqui" # Ou service_role_key
supabase: Client = create_client(supabase_api_url, supabase_api_key)

# --- Parte 2: SQLAlchemy (Para o ORM com FastAPI) ---
# Isso é para conectar o SQLAlchemy direto no banco PostgreSQL.

# PEGUE SUA SENHA NO PAINEL DO SUPABASE!
DB_PASSWORD = "SUA_SENHA_DO_BANCO_AQUI" 
DB_URL = f"postgresql://postgres:{DB_PASSWORD}@db.xomisypdbkawfgzsddwn.supabase.co:5432/postgres"

# Agora use a URL correta no create_engine
engine = create_engine(
    DB_URL,
    pool_pre_ping=True,
)

#############################################################
# O resto do seu código estava certo:
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

print("Configuração do SQLAlchemy e Supabase Client pronta!")



"""