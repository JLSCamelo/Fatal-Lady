document.getElementById("cep-input").addEventListener("input", function () {
    const cep = this.value;
    const btn = document.getElementById("calculate-shipping-btn");

});

document.getElementById("calculate-shipping-btn").addEventListener("click", async function () {
    const cep = document.getElementById("cep-input").value;
    const resultsDiv = document.getElementById("shipping-results");

    try {
        const response = await fetch(`/frete/calcular/${cep}`);
        if (!response.ok) throw new Error("Erro na requisição");

        const data = await response.json();

        resultsDiv.innerHTML = `
            <p><strong>Frete:</strong> R$ ${data.frete}</p>
            <p><strong>Prazo:</strong> ${data.prazo} dias</p>
        `;
    } catch (err) {
        resultsDiv.innerHTML = `<p>Erro ao calcular frete.</p>`;
    }
});
