const shippingButton = document.getElementById("calculate-shipping-btn");

async function calcularFrete() {
  const cepInput = document.getElementById("cep-input");
  if (!cepInput) return;

  const cep = cepInput.value.trim().replace(/\D/g, "");

  if (cep.length !== 8) {
    alert("Digite um CEP válido com 8 dígitos.");
    return;
  }

  try {
    const response = await fetch(`/frete/calcular/?cep_destino=${encodeURIComponent(cep)}`);

    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      throw new Error(error.detail || "Erro ao consultar o frete.");
    }
    const data = await response.json();

    const results = document.getElementById("shipping-results");
    if (results) results.style.display = "block";

    const endereco = document.getElementById("endereco");
    if (endereco) endereco.innerText = data.endereco;

    const valorFrete = document.getElementById("valor_frete");
    if (valorFrete) valorFrete.innerText = Number(data.valor_frete).toFixed(2);

    const prazo = document.getElementById("prazo");
    if (prazo) prazo.innerText = data.prazo_estimado_dias;

    const subtotalEl = document.getElementById("subtotal");
    const totalEl = document.getElementById("total");
    if (subtotalEl && totalEl) {
      const subtotal = parseFloat(subtotalEl.innerText);
      const total = subtotal + Number(data.valor_frete);
      totalEl.innerText = total.toFixed(2);
    }
    const cepHidden = document.getElementById("cepHidden");
    const enderecoHidden = document.getElementById("enderecoHidden");
    const freteHidden = document.getElementById("freteHidden");
    const totalHidden = document.getElementById("totalHidden");

    if (cepHidden) cepHidden.value = cep;
    if (enderecoHidden) enderecoHidden.value = data.endereco;
    if (freteHidden) freteHidden.value = Number(data.valor_frete).toFixed(2);

    if (totalHidden && totalEl) {
      totalHidden.value = totalEl.innerText;
    }
  } catch (error) {
    console.error(error);
    alert(error.message || "Erro ao calcular o frete. Tente novamente.");
  }
}

if (shippingButton) {
  shippingButton.addEventListener("click", (event) => {
    event.preventDefault();
    calcularFrete();
  });
}