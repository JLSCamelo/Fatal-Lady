from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.controllers.excluir_conta_controller import *
from app.auth import verificar_token, verificar_senha
from app.ultils import enviar_email

router = APIRouter(prefix="/excluir", tags=["Usuários"])

@router.delete("/conta")
def delete_account(request: Request, db: Session = Depends(get_db)):
    return exlcuir_conta(request, db)




@router.post("/conta")
async def solicitar_exclusao(request: Request, db: Session = Depends(get_db)):
    usuario = request.state.usuario  # supondo que o usuário esteja autenticado

    if not usuario:
        raise HTTPException(status_code=401, detail="Usuário não autenticado")

    token = verificar_token(usuario.email, exp_minutos=30)
    link_confirmacao = f"{request.base_url}excluir/confirmar/{token}"

    enviar_email(
        destinatario=usuario.email,
        assunto="Confirmação de Exclusão de Conta",
        corpo=f"""
        Olá {usuario.nome},<br><br>
        Recebemos uma solicitação para excluir sua conta.<br>
        Para confirmar, clique no link abaixo (válido por 30 minutos):<br><br>
        <a href="{link_confirmacao}">Clic=que no link para confirmação</a>
        """
    )
    return {"message": "E-mail de confirmação enviado"}

from fastapi import Request, Form
from fastapi.responses import HTMLResponse

@router.get("/confirmar/{token}", response_class=HTMLResponse)
async def confirmar_exclusao_get(request: Request, token: str):
    email = verificar_token(token)
    if not email:
        return HTMLResponse("<h3>Link inválido ou expirado.</h3>")

    html = f"""
    <h2>Confirmação de Exclusão de Conta</h2>
    <form method="post" action="/excluir/confirmar/{token}">
        <label>CPF:</label><input type="text" name="cpf" required><br>
        <label>Data de nascimento:</label><input type="date" name="data_nascimento" required><br>
        <label>Senha:</label><input type="password" name="senha" required><br>
        <button type="submit">Confirmar exclusão</button>
    </form>
    """
    return HTMLResponse(content=html)


@router.post("/confirmar/{token}")
def confirmar_exclusao_post(
    token: str,
    cpf: str = Form(...),
    data_nascimento: str = Form(...),
    senha: str = Form(...),
    db: Session = Depends(get_db)
):
    email = verificar_token(token)
    if not email:
        raise HTTPException(status_code=400, detail="Link inválido ou expirado")

    usuario = db.query(UsuarioDB).filter_by(email=email).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    if usuario.cpf != cpf or str(usuario.data_nascimento) != data_nascimento:
        raise HTTPException(status_code=400, detail="Dados incorretos")

    if not verificar_senha(senha, usuario.senha_hash):
        raise HTTPException(status_code=401, detail="Senha incorreta")

    db.delete(usuario)
    db.commit()
    return {"message": "Conta excluída com sucesso"}




