import smtplib

import os
from dotenv import load_dotenv
from email.mime.text import MIMEText


load_dotenv()
EMAIL_REMITENTE = os.getenv("EMAIL_REMITENTE")
EMAIL_SENHA = os.getenv("EMAIL_SENHA")
EMAIL_FROM_NAME = os.getenv("EMAIL_FROM_NAME", EMAIL_REMITENTE)



def enviar_email(destinatario, assunto, corpo):
    msg = MIMEText(corpo, "html")
    msg["Subject"] = assunto
    msg["From"] = "fatallady@gmail.com.br"
    msg["To"] = destinatario

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(EMAIL_REMITENTE,EMAIL_SENHA)
        server.send_message(msg)
