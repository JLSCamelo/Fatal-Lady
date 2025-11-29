// Pega referências dos campos
const cepInput = document.getElementById("cep");
const ruaInput = document.getElementById("rua");
const bairroInput = document.getElementById("bairro");
const cidadeInput = document.getElementById("cidade");
const estadoInput = document.getElementById("estado");

// =============== MÁSCARA DO CEP ===============
if (cepInput) {
  cepInput.addEventListener("input", function (e) {
    let value = e.target.value.replace(/\D/g, ""); // só números

    if (value.length > 8) value = value.slice(0, 8); // limite 8 dígitos

    if (value.length > 5) {
      value = value.slice(0, 5) + "-" + value.slice(5); // 00000-000
    }

    e.target.value = value;
  });

  // =============== BLUR: CHAMAR SEU BACKEND ===============
  cepInput.addEventListener("blur", async function () {
    const cep = this.value.replace(/\D/g, "");

    if (cep.length !== 8) {
      alert("CEP inválido. Digite um CEP com 8 números.");
      return;
    }

    try {
      const response = await fetch(`/frete/completar_cadastro/${cep}`);
      if (!response.ok) throw new Error("Erro ao buscar CEP");

      const data = await response.json();

      // Ajuste os nomes das propriedades conforme o que seu backend retorna
      if (ruaInput) ruaInput.value = data.rua || "";
      if (bairroInput) bairroInput.value = data.bairro || "";
      if (cidadeInput) cidadeInput.value = data.cidade || "";
      if (estadoInput) estadoInput.value = data.estado || "";
    } catch (error) {
      console.error(error);
      alert(
        "Não foi possível buscar o endereço. Verifique o CEP e tente novamente."
      );
    }
  });
}
