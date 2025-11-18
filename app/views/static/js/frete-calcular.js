// // 1 Adiciona um "ouvinte" de evento (event listener) ao botão com id="btnCalcularFrete"
//   // Ou seja, quando o botão for clicado, o código dentro da função será executado.
//   document.getElementById("btnCalcularFrete").addEventListener("click", async () => {
    
//     try {
//       // 4 Busca o token do usuário no armazenamento local (salvo no navegador)
//       // Isso serve para autenticação — o mesmo que usar um token JWT no header.
//       const token = localStorage.getItem("token");

//       // 5 Faz a requisição para o backend (sem recarregar a página)
//       // O `fetch` é o equivalente em JS ao `requests.get()` em Python.
//       const response = await fetch(`/frete/calcular/?cep_destino=${cep}`, {
//         headers: { "Authorization": `Bearer ${token}` } // Envia o token no cabeçalho
//       });

//       // 6 Se a resposta não for 200 (OK), lança erro
//       if (!response.ok) throw new Error("Erro ao consultar o frete.");

//       // 7 Converte o JSON da resposta em um objeto JavaScript
//       // É como usar `response.json()` no Python requests.
//       const data = await response.json();

//       // 8 Torna a área de resultado visível
//       document.getElementById("resultadoFrete").style.display = "block";

//       // 9 Atualiza as informações visuais com o retorno do backend
//       document.getElementById("endereco").innerText = data.endereco;
//       document.getElementById("valor_frete").innerText = data.valor_frete.toFixed(2);
//       document.getElementById("prazo").innerText = data.prazo_estimado_dias;

//       // 10 Atualiza o valor total do pedido (subtotal + frete)
//       const subtotal = parseFloat(document.getElementById("subtotal").innerText);
//       const total = subtotal + data.valor_frete;
//       document.getElementById("total").innerText = total.toFixed(2);

//       // 11 Atualiza os campos ocultos do formulário HTML
//       // Assim, quando o usuário clicar em “Finalizar Compra”, o backend receberá tudo.
//       document.getElementById("cepHidden").value = cep;
//       document.getElementById("enderecoHidden").value = data.endereco;
//       document.getElementById("freteHidden").value = data.valor_frete.toFixed(2);
//       document.getElementById("totalHidden").value = total.toFixed(2);

//     } catch (error) {
//       // 12 Caso aconteça qualquer erro (problema de rede, API, etc.)
//       alert("Erro ao calcular o frete. Tente novamente.");
//     }
//   });
document.getElementById("btnCalcularFrete").addEventListener("click", async () => {
  const cep = (typeof cepUsuario === "string" ? cepUsuario.trim() : "");

  if (!cep) {
    alert("CEP do usuário não encontrado.");
    return;
  }

  try {
    const response = await fetch(`/frete/calcular/?cep_destino=${encodeURIComponent(cep)}`, {
      method: "GET",
      credentials: "include"
    });

    if (!response.ok) {
      throw new Error("Erro ao consultar o frete.");
    }

    const data = await response.json();

    // Mostra área de frete
    const resultadoFreteEl = document.getElementById("resultadoFrete");
    if (resultadoFreteEl) {
      resultadoFreteEl.style.display = "block";
    }

    // Frete como número
    let valorFrete = Number(data.valor_frete);
    if (Number.isNaN(valorFrete)) {
      valorFrete = Number(String(data.valor_frete).replace(",", ".")) || 0;
    }

    document.getElementById("endereco").innerText = data.endereco;
    document.getElementById("valor_frete").innerText = valorFrete.toFixed(2);
    document.getElementById("prazo").innerText = data.prazo_estimado_dias + " dias";

    // Subtotal
    const subtotalEl = document.getElementById("subtotal");
    let subtotal = Number(subtotalEl?.dataset?.valor);

    if (Number.isNaN(subtotal)) {
      const subtotalText = subtotalEl.innerText
        .replace("R$", "")
        .replace(/\s/g, "")
        .replace(".", "")
        .replace(",", ".");
      subtotal = parseFloat(subtotalText) || 0;
    }

    const total = subtotal + valorFrete;

    console.log("DEBUG subtotal:", subtotal, "frete:", valorFrete, "total:", total);

    document.getElementById("total").innerText = "R$ " + total.toFixed(2);

    document.getElementById("cepHidden").value = cep;
    document.getElementById("enderecoHidden").value = data.endereco;
    document.getElementById("freteHidden").value = valorFrete.toFixed(2);
    document.getElementById("totalHidden").value = total.toFixed(2);

  } catch (error) {
    console.error(error);
    alert("Erro ao calcular o frete. Tente novamente.");
  }
});
