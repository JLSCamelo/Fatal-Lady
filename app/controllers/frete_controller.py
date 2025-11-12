import requests
from fastapi import HTTPException, Request
from app.auth import verificar_token

CEP_LOJA = "03008020"  # CEP SENAI

def controller_calcular_frete(request: Request, cep_destino: str):
    token = request.cookies.get("token")
    payload = verificar_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Usuário não autenticado")

    # validação simples de CEP
    if not cep_destino.isdigit() or len(cep_destino) != 8:
        raise HTTPException(status_code=400, detail="CEP inválido")

    # consulta no ViaCep
    via_cep_url = f"https://viacep.com.br/ws/{cep_destino}/json/"
    resposta = requests.get(via_cep_url)
    if resposta.status_code != 200:
        raise HTTPException(status_code=400, detail="Erro ao consultar o CEP")

    dados = resposta.json()
    if "erro" in dados:
        raise HTTPException(status_code=400, detail="CEP não encontrado")

    # simulação do frete com dados fixos
    valor_frete = 15.00
    prazo_estimado = 6

    return {
        "endereco": f"{dados.get('logradouro')}, {dados.get('bairro')}, "
                    f"{dados.get('localidade')}, {dados.get('uf')}",
        "cep": cep_destino,
        "valor_frete": valor_frete,
        "prazo_estimado_dias": prazo_estimado,
        "status": "simulação concluída"
    }


def controller_completar_cadastro(cep_destino: str):
    # validação simples de CEP
    if not cep_destino.isdigit() or len(cep_destino) != 8:
        raise HTTPException(status_code=400, detail="CEP inválido")

    # consulta no ViaCep
    via_cep_url = f"https://viacep.com.br/ws/{cep_destino}/json/"
    resposta = requests.get(via_cep_url)

    if resposta.status_code != 200:
        raise HTTPException(status_code=400, detail="Erro ao consultar o CEP")

    dados = resposta.json()
    if "erro" in dados:
        raise HTTPException(status_code=400, detail="CEP não encontrado")

    return {
        "cep": cep_destino,
        "rua": dados.get("logradouro", ""),
        "bairro": dados.get("bairro", ""),
        "estado": dados.get("uf", ""),
        "cidade": dados.get("localidade", "")
    }
