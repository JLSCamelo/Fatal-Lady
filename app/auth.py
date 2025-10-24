# auth.py
from datetime import datetime, timedelta
import os
from typing import Optional, Dict, Any

from jose import JWTError, jwt
from passlib.context import CryptContext

# Configurações (use variáveis de ambiente em produção)
SECRET_KEY: str = os.getenv("SECRET_KEY", "chave-secreta")
ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_MINUTES: int = int(os.getenv("ACCESS_TOKEN_MINUTES", "30"))

# CryptContext: prioriza bcrypt_sha256 (evita limite 72 bytes), mantém bcrypt para compatibilidade.
pwd_context = CryptContext(schemes=["bcrypt_sha256", "bcrypt"], default="bcrypt_sha256", deprecated="auto")

# ---------------------- Funções de senha ----------------------
def gerar_hash_senha(senha: str) -> str:
    """Gera hash para a senha informada (string)."""
    return pwd_context.hash(senha)

def verificar_senha(senha: str, senha_hash: str) -> bool:
    """Verifica senha contra o hash armazenado."""
    return pwd_context.verify(senha, senha_hash)

def needs_rehash(senha_hash: str) -> bool:
    """Retorna True se o hash precisa ser atualizado (e.g. mudou o esquema/parametros)."""
    return pwd_context.needs_update(senha_hash)

def rehash_password_if_needed(plain_password: str, senha_hash: str) -> Optional[str]:
    """
    Se o hash precisa de atualização, retorna o novo hash (para salvar no DB). Caso contrário, retorna None.
    """
    if needs_rehash(senha_hash):
        return gerar_hash_senha(plain_password)
    return None

# ---------------------- JWT (token) ----------------------
def criar_token(dados: Dict[str, Any], expires_minutes: int = ACCESS_TOKEN_MINUTES) -> str:
    """Cria JWT com expiração. `dados` é uma dict de claims (ex: {'sub': email})."""
    dados_token = dados.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    dados_token.update({"exp": expire})
    token_jwt = jwt.encode(dados_token, SECRET_KEY, algorithm=ALGORITHM)
    return token_jwt

def verificar_token(token: str) -> Optional[Dict[str, Any]]:
    """Decodifica e valida token JWT. Retorna payload se válido, ou None se inválido/expirado."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

# ---------------------- Helper opcional (não recomendado) ----------------------
def _truncate_password_bytes(password: str, max_bytes: int = 72) -> str:
    """
    Trunca a senha em bytes sem quebrar a decodificação UTF-8 (apenas se for absolutamente necessário).
    Prefira NÃO usar truncamento e sim bcrypt_sha256.
    """
    b = password.encode("utf-8")
    if len(b) <= max_bytes:
        return password
    truncated = b[:max_bytes]
    return truncated.decode("utf-8", errors="ignore")
