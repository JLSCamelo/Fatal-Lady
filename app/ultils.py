import smtplib
import re
import os
from dotenv import load_dotenv
from email.mime.text import MIMEText


load_dotenv()
EMAIL_REMITENTE = os.getenv("EMAIL_REMITENTE")
EMAIL_SENHA = os.getenv("EMAIL_SENHA")
EMAIL_FROM_NAME = os.getenv("EMAIL_FROM_NAME", EMAIL_REMITENTE)



def validar_cpf(cpf: str) -> bool: #bool: faz retornar True ou False
    #remove tudo que não for número
    #\D: qualquer coisa que não seja numero
    #\d: qualquer numero de 0 a 9
    #função re substitui "x" por "y"
    cpf = str(cpf)
    cpf = re.sub(r"\D", "", cpf)

    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False
    
    #fazendo calculo par ver se é valido o cpf
    for i in range(9, 11):
        soma = sum(int(cpf[j]) * ((i + 1) - j) for j in range(i))
        digito = (soma * 10 % 11) % 10
        if digito != int(cpf[i]):
            return False
    return True

def enviar_email(destinatario, assunto, corpo):
    msg = MIMEText(corpo, "html")
    msg["Subject"] = assunto
    msg["From"] = "fatallady@gmail.com.br"
    msg["To"] = destinatario

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(EMAIL_REMITENTE,EMAIL_SENHA)
        server.send_message(msg)

"""
465	cmc ja criptografado
587	criptografa após starttls	
"""



from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from app.database import SessionLocal
from app.models.usuario_model import UsuarioDB

def verificar_inativos():
    db = SessionLocal()
    limite = datetime.utcnow() - timedelta(days=30)

    inativos = db.query(UsuarioDB).filter(UsuarioDB.ultima_atividade < limite).all()

    for user in inativos:
        enviar_email(
            user.email,
            assunto="Sentimos sua falta 💛",
            corpo="""
        Olá! Faz 1 mês que você não acessa nossa plataforma.

        Estamos com novidades incríveis esperando por você!

        Clique para voltar ➜  http://127.0.0.1:8000
        """
                     )

    db.close()


scheduler = BackgroundScheduler()
# scheduler.add_job(verificar_inativos, "interval", seconds=10)  # executa todo dia às 00:00
scheduler.add_job(verificar_inativos, "cron", hour=0)
scheduler.start()
