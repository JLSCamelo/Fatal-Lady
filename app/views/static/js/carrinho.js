document.addEventListener("DOMContentLoaded", () => {
  // Seleciona todos os formulários de atualização de item
  const updateForms = document.querySelectorAll(".form-update-cart");

  updateForms.forEach(form => {
    const qtyInput = form.querySelector(".input-quantity");
    const btnMinus = form.querySelector(".btn-qty-minus");
    const btnPlus = form.querySelector(".btn-qty-plus");

    // Função para submeter o formulário
    const submitForm = () => {
      // Adiciona um feedback visual de "carregando"
      // Reutiliza a classe .removing que você já tem no CSS
      const cartItem = form.closest('.cart-item');
      if (cartItem) {
        cartItem.classList.add('removing'); // Fica semitransparente
      }
      
      // Envia o formulário (isso causará um recarregamento da página)
      form.submit();
    };

    // ---- OUVINTES DE EVENTOS ----

    // 1. Clique no Botão de Mais
    btnPlus.addEventListener("click", () => {
      qtyInput.value = parseInt(qtyInput.value, 10) + 1;
      submitForm(); // Envia o formulário
    });

    // 2. Clique no Botão de Menos
    btnMinus.addEventListener("click", () => {
      let currentValue = parseInt(qtyInput.value, 10);
      if (currentValue > 1) {
        qtyInput.value = currentValue - 1;
        submitForm(); // Envia o formulário
      }
      // Se for 1 e clicar menos, não faz nada
    });

    // 3. Mudar manualmente e teclar 'Enter' ou sair do campo
    qtyInput.addEventListener("change", () => {
      let currentValue = parseInt(qtyInput.value, 10);
      if (currentValue < 1 || isNaN(currentValue)) {
        qtyInput.value = 1; // Reseta para 1 se for inválido
      }
      submitForm(); // Envia o formulário
    });
  });
});