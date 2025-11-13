import re
from app.models.usuario_model import UsuarioDB
from app.models.enderecos_model import EnderecoDB
from app.database import *
from app.auth import *
from fastapi import Request
from datetime import date
from sqlalchemy.orm import Session
import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv
from app.ultils import enviar_email

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
                        cpf: str,
                        genero: str,
                        data_nascimento: date,
                        bairro: str,
                        estado:str,
                        numero: str,
                        db: Session):
    # Verifica se o e-mail já existe
    usuario = db.query(UsuarioDB).filter(UsuarioDB.email == email).first()
    if usuario:
        return {"mensagem": "E-mail já cadastrado"}
    
    validator=validar_cpf(cpf)
    if validator == False:
        return  {"mensagem": "cpf invalido!"}


    # Cria o hash da senha e salva o usuário
    senha_hash = gerar_hash_senha(senha)
    novo_usuario = UsuarioDB(
        nome=nome,
        email=email,
        senha=senha_hash,
        telefone=telefone,
        cpf=cpf,
        genero=genero,
        data_nascimento=data_nascimento
    )
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)

    # Cria o endereço vinculado
    novo_endereco = EnderecoDB(
        usuario_id=novo_usuario.id_cliente,
        cep=cep,
        rua=rua,
        bairro=bairro,
        cidade=cidade,
        estado=estado,
        complemento=complemento,
        numero=numero
    )

    db.add(novo_endereco)
    db.commit()

    # Envia e-mail de boas-vindas
    try:
      enviar_email(
          destinatario=usuario.email,
          assunto="Bem vindo a Fatal Lady", 
          corpo=
           f"""
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
              <h2>Olá, {nome}! 👋</h2>
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
    </html>""")
      # enviar_email_boas_vindas(email, nome)
    except Exception:
         return {"mensagem": "Erro ao cadastrar user"}

    return {"mensagem": "Usuário cadastrado com sucesso!"}



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