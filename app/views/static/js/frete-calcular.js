const calculateShippingButton = document.getElementById("calculate-shipping-btn");
const shippingResults = document.getElementById("shipping-results");
const enderecoElement = document.getElementById("endereco");
const valorFreteElement = document.getElementById("valor_frete");
const prazoElement = document.getElementById("prazo");
const subtotalElement = document.getElementById("subtotal");
const totalElement = document.getElementById("total");
const cepHidden = document.getElementById("cepHidden");
const enderecoHidden = document.getElementById("enderecoHidden");
const freteHidden = document.getElementById("freteHidden");
const totalHidden = document.getElementById("totalHidden");

function parseCurrency(text) {
  const normalized = text?.replace(/[^0-9.,-]/g, "").replace(",", ".");
  return parseFloat(normalized) || 0;
}

if (calculateShippingButton) {
  calculateShippingButton.addEventListener("click", async () => {
    const cepInput = document.getElementById("cep-input");
    const cep = cepInput ? cepInput.value.trim() : "";

    if (cep.length !== 8) {
      alert("Digite um CEP válido com 8 dígitos.");
      return;
    }

    try {
      const token = localStorage.getItem("token")
      const response = await fetch(`/frete/calcular/?cep_destino=${encodeURIComponent(cep)}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
    
      if (!response.ok) throw new Error("Erro ao consultar o frete.");

       const data = await response.json();
      if (shippingResults) shippingResults.style.display = "block";
      if (enderecoElement) enderecoElement.innerText = data.endereco;
      if (valorFreteElement) valorFreteElement.innerText = data.valor_frete.toFixed(2);
      if (prazoElement) prazoElement.innerText = data.prazo_estimado_dias;
      const total = subtotal + data.valor_frete;
      if (totalElement) totalElement.innerText = `R$ ${total.toFixed(2)}`;

      if (cepHidden) cepHidden.value = cep;
      if (enderecoHidden) enderecoHidden.value = data.endereco;
      if (freteHidden) freteHidden.value = data.valor_frete.toFixed(2);
      if (totalHidden) totalHidden.value = total.toFixed(2);
    } catch (error) {
      // 12 Caso aconteça qualquer erro (problema de rede, API, etc.)
      alert("Erro ao calcular o frete. Tente novamente.");
    }
  });
}