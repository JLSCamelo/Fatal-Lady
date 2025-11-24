from datetime import datetime, timedelta
import os
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from passlib.context import CryptContext

SECRET_KEY: str = os.getenv("SECRET_KEY", "chave-secreta")
ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_MINUTES: int = int(os.getenv("ACCESS_TOKEN_MINUTES", "30"))

# CryptContext: prioriza bcrypt_sha256 (evita limite 72 bytes), mantém bcrypt para compatibilidade.
pwd_context = CryptContext(schemes=["bcrypt_sha256", "bcrypt"], default="bcrypt_sha256", deprecated="auto")

#Cria hash
def gerar_hash_senha(senha: str) -> str:
    return pwd_context.hash(senha)

#Verifica senha
def verificar_senha(senha: str, senha_hash: str) -> bool:
    return pwd_context.verify(senha, senha_hash)

#Verifica se precisa atualizar hash
def needs_rehash(senha_hash: str) -> bool:
    return pwd_context.needs_update(senha_hash)

#Atualiza o hash
def rehash_password_if_needed(plain_password: str, senha_hash: str) -> Optional[str]:
    if needs_rehash(senha_hash):
        return gerar_hash_senha(plain_password)
    return None

#Cria token
def criar_token(dados: Dict[str, Any], expires_minutes: int = ACCESS_TOKEN_MINUTES) -> str:
    dados_token = dados.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    dados_token.update({"exp": expire})
    token_jwt = jwt.encode(dados_token, SECRET_KEY, algorithm=ALGORITHM)
    return token_jwt

#Verifica token
def verificar_token(token: str):
    if not token:
        return None
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except (JWTError, TypeError):
        return None
