# importar requests,math, HTTPException,Querry
from fastapi import APIRouter,Request,Form,UploadFile,File,Depends,HTTPException,Query
from app.auth import verificar_token
import requests, math


router = APIRouter()
CEP_LOJA="03008020"#CEP SENAI

@router.get("/api/frete")
def calcular_frete(request:Request,
    cep_destino:str=Query(...)):

    token=request.cookies.get("token")
    payload=verificar_token(token)
    if not payload:
        raise HTTPException(status_code=401,
            detail="Usuário não autenticado")
    
   #validação simples de cep
    if not cep_destino.isdigit() or len(cep_destino) !=8:
        raise HTTPException(status_code=400,
                detail="CEP inválido")
    
    #consulta no ViaCep
    via_cep_url=f"https://viacep.com.br/ws/{cep_destino}/json/"
    resposta= requests.get(via_cep_url)
    if resposta.status_code !=200:
        raise HTTPException(status_code=400,
                detail="Erro ao consultar o CEP")
    
    dados=resposta.json()
    if "erro" in dados:
        raise HTTPException(status_code=400,
            detail="CEP não encontrado")
    
    #simulação do frete com dados fixo
    valor_frete =15.00
    prazo_estimado=6
    
    #retorno dados estruturado endereço via cep
    return {
        "endereco":f"{dados.get('logradouto')},{dados.get('bairro')},{dados.get('localidade')},{dados.get('uf')}",
        "cep":cep_destino,
        "valor_frete":valor_frete,
        "prazo_estimado_dias":prazo_estimado,
        "status":"simulação concluída"}

#####################################################################
#####################################################################
"""
<!--carrinho.html-->
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <title>Checkout</title>
</head>
<body>
  <h2>Finalizar Compra</h2>

  {% if carrinho %}
    <ul>
      {% for item in carrinho %}
        <li>{{ item.nome }} - {{ item.quantidade }} x R$ {{ item.preco }}</li>
      {% endfor %}
    </ul>
    <p><b>Subtotal:</b> R$ <span id="subtotal">{{ total }}</span></p>
  {% else %}
    <p>Seu carrinho está vazio.</p>
  {% endif %}

  <hr>


  <!-- Simulação de frete -->
  <label>Digite o CEP:</label>
  <input type="text" id="cep" maxlength="8" placeholder="Ex: 01001000">
  <button type="button" id="btnCalcularFrete">Calcular Frete</button>

  <div id="resultadoFrete" style="display:none; margin-top:10px;">
    <p><b>Endereço:</b> <span id="endereco"></span></p>
    <p><b>Frete:</b> R$ <span id="valor_frete"></span></p>
    <p><b>Prazo:</b> <span id="prazo"></span> dias</p>
  </div>

  <hr>
  <p><b>Total com frete:</b> R$ <span id="total">{{ total }}</span></p>

  <!-- Formulário real de finalização -->
  <form id="formCheckout" action="/checkout" method="post">
    <input type="hidden" name="cep" id="cepHidden">
    <input type="hidden" name="endereco" id="enderecoHidden">
    <input type="hidden" name="frete" id="freteHidden">
    <input type="hidden" name="total" id="totalHidden">
    <button type="submit">Finalizar Compra</button>
  </form>

  <a href="/">Voltar à loja</a>

  <script>
  // 1 Adiciona um "ouvinte" de evento (event listener) ao botão com id="btnCalcularFrete"
  // Ou seja, quando o botão for clicado, o código dentro da função será executado.
  document.getElementById("btnCalcularFrete").addEventListener("click", async () => {

    // 2 Pega o valor do campo de CEP (input com id="cep")
    const cep = document.getElementById("cep").value.trim(); // trim() remove espaços extras

    // 3 Verifica se o CEP tem exatamente 8 dígitos
    if (cep.length !== 8) {
      alert("Digite um CEP válido com 8 dígitos."); // Exibe alerta caso seja inválido
      return; // Sai da função (não continua)
    }

    try {
      // 4 Busca o token do usuário no armazenamento local (salvo no navegador)
      // Isso serve para autenticação — o mesmo que usar um token JWT no header.
      const token = localStorage.getItem("token");

      // 5 Faz a requisição para o backend (sem recarregar a página)
      // O `fetch` é o equivalente em JS ao `requests.get()` em Python.
      const response = await fetch(`/api/frete?cep_destino=${cep}`, {
        headers: { "Authorization": `Bearer ${token}` } // Envia o token no cabeçalho
      });

      // 6 Se a resposta não for 200 (OK), lança erro
      if (!response.ok) throw new Error("Erro ao consultar o frete.");

      // 7 Converte o JSON da resposta em um objeto JavaScript
      // É como usar `response.json()` no Python requests.
      const data = await response.json();

      // 8 Torna a área de resultado visível
      document.getElementById("resultadoFrete").style.display = "block";

      // 9 Atualiza as informações visuais com o retorno do backend
      document.getElementById("endereco").innerText = data.endereco;
      document.getElementById("valor_frete").innerText = data.valor_frete.toFixed(2);
      document.getElementById("prazo").innerText = data.prazo_estimado_dias;

      // 10 Atualiza o valor total do pedido (subtotal + frete)
      const subtotal = parseFloat(document.getElementById("subtotal").innerText);
      const total = subtotal + data.valor_frete;
      document.getElementById("total").innerText = total.toFixed(2);

      // 11 Atualiza os campos ocultos do formulário HTML
      // Assim, quando o usuário clicar em “Finalizar Compra”, o backend receberá tudo.
      document.getElementById("cepHidden").value = cep;
      document.getElementById("enderecoHidden").value = data.endereco;
      document.getElementById("freteHidden").value = data.valor_frete.toFixed(2);
      document.getElementById("totalHidden").value = total.toFixed(2);

    } catch (error) {
      // 12 Caso aconteça qualquer erro (problema de rede, API, etc.)
      alert("Erro ao calcular o frete. Tente novamente.");
    }
  });
</script>
</body>
</html>"""