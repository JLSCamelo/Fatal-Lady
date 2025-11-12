from app.models.usuario_model import UsuarioDB
from app.database import *
from app.auth import *
from fastapi import Request
from sqlalchemy.orm import Session
import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv

load_dotenv()
EMAIL_REMITENTE = os.getenv("EMAIL_REMITENTE")
EMAIL_SENHA = os.getenv("EMAIL_SENHA")
EMAIL_FROM_NAME = os.getenv("EMAIL_FROM_NAME", EMAIL_REMITENTE)


def cadastro_controller(request: Request,
                        nome: str,
                        email: str,
                        senha: str,
                        cep: str,
                        rua: str,
                        cidade: str,
                        telefone: str,
                        complemento: str,
                        cpf: int,
                        genero: str,
                        data_nascimento: datetime,
                        bairro: str,
                        estado:str,
                        db: Session):
    # Verifica se o e-mail já existe
    usuario = db.query(UsuarioDB).filter(UsuarioDB.email == email).first()
    if usuario:
        return {"mensagem": "E-mail já cadastrado"}

    # Cria o hash da senha e salva o usuário
    senha_hash = gerar_hash_senha(senha)
    novo_usuario = UsuarioDB(
        nome=nome,
        email=email,
        senha=senha_hash,
        cep=cep,
        rua=rua,
        cidade=cidade,
        telefone=telefone,
        complemento=complemento,
        cpf=cpf,
        genero=genero,
        data_nascimento=data_nascimento,
        bairro=bairro,
        estado=estado
    )
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)

    # Envia e-mail de boas-vindas
    try:
        enviar_email_boas_vindas(email, nome)
    except Exception:
         return {"mensagem": "Erro ao cadastrar user"}

    return {"mensagem": "Usuário cadastrado com sucesso!"}


def enviar_email_boas_vindas(destinatario: str, nome_usuario: str):
    if not EMAIL_REMITENTE or not EMAIL_SENHA:
        raise RuntimeError("Configurações de e-mail não definidas. Verifique o .env")

    msg = EmailMessage()
    msg["Subject"] = "👠 Bem-vindo(a) à Fatal Lady!"
    msg["From"] = EMAIL_FROM_NAME
    msg["To"] = destinatario

    # Corpo em texto (fallback)
    msg.set_content(f"Olá {nome_usuario}, seja bem-vinda à Fatal Lady!")

    # Corpo em HTML
    html_content = f"""
    <html>
      <body style="margin:0; padding:0; font-family:'Poppins',Arial,sans-serif; background-color:#fff;">
        <table width="100%" cellpadding="0" cellspacing="0">
          <tr>
            <td align="center" style="padding:40px 0;">
              <img src="views/static/upload/img/catalogo/icons-main/letreiro-logo.png" width="80" alt="Fatal Lady">
              <h1 style="color:#000; font-size:28px; margin-top:10px;">FATAL <span style="color:#d00000;">LADY</span></h1>
            </td>
          </tr>
          <tr>
            <td align="center" style="padding:20px 40px;">
              <h2>Olá, {nome_usuario}! 👋</h2>
              <p>Seja muito bem-vinda à <b>Fatal Lady</b> — onde a elegância encontra a atitude.</p>
              <p>Explore nossa coleção de saltos finos e sandálias exclusivas!</p>
              <a href="http://127.0.0.1:8000/login" style="display:inline-block; margin-top:20px; background-color:#d00000; color:#fff; padding:14px 28px; border-radius:4px; text-decoration:none; font-weight:bold;">
                Descubra Agora
              </a>
            </td>
          </tr>
          <tr>
            <td align="center" style="padding:40px 0; background-color:#000; color:#fff; font-size:13px;">
              <p>Frete grátis em compras acima de R$299</p>
              <p>© 2025 Fatal Lady. Todos os direitos reservados.</p>
            </td>
          </tr>
        </table>
      </body>
    </html>
    """
    msg.add_alternative(html_content, subtype="html")

    # Envia o e-mail
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_REMITENTE, EMAIL_SENHA)
        smtp.send_message(msg)