from datetime import datetime,timedelta
#datetime=ano,mes,dia,hora,min,segundo
#timedelta=adição ou subrtraçãp de tempo ou data

from jose import JWSError, jwt
#jose - JavaScript object signing and encrytion
#jwtErro = erro de criptografia
#jwt = json web token, assinatura assinada entre duas partes

from passlib.context import CryptContext
#implementação de contexto de criptografia, verifica o hash da senha

#criar a chave secreta do token (em produto guardar em .env)
SECRET_KEY="chave-secreta"
ALGORITHM="HS256"
'''
HS256 - algoritmo de criptografia de 256 bits vai criar um hash
'chave-screta', a mesma chave é usada para assinar o jwt e
verificar assinatura do cliente
'''
ACESS_TOKEN_MINUTES=30 #token de tempo 30 minutos

#criptografia de senha
pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto") #bcrypt - mecanismo de criptografia

#criar hash
def gerar_hash_senha(senha:str):
    return pwd_context.hash(senha)

#verificar senha
def verificar_senha(senha:str,senha_hash:str):
    return pwd_context.verify(senha,senha_hash)

#criar token
def criar_token(dados:dict):
    dados_token=dados.copy()
    token_jwt=jwt.encode(dados_token,SECRET_KEY,algorithm=ALGORITHM)
    return token_jwt

#verificar o token payload=carga útil
def verificar_token(token:str):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        return payload
    except JWSError:
        return None