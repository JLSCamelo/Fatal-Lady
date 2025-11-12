document.addEventListener("DOMContentLoaded", () => {
  
  // --- INÍCIO DA LÓGICA DE CONTAGEM (QUE FALTAVA) ---
  const updateLocalStorageCount = () => {
    // Busca todos os itens visíveis na página
    const allItems = document.querySelectorAll(".cart-item");
    let totalCount = 0;

    if (allItems.length > 0) {
      // Itera em cada item para somar as quantidades
      allItems.forEach(item => {
        // Usa as classes do seu HTML
        const qtyInput = item.querySelector(".input-quantity"); 
        if (qtyInput) {
          totalCount += parseInt(qtyInput.value, 10) || 0;
        }
      });
    }
    // Se .cart-item não for encontrado (carrinho vazio), totalCount será 0.

    // Salva o total calculado no localStorage
    localStorage.setItem("cartItemCount", totalCount);
    
    // Dispara um evento para o 'cart-badge.js' (Exibidor) ler o novo valor imediatamente
    window.dispatchEvent(new Event('cartUpdated'));
  };

  // Calcula e salva o total assim que a página do carrinho carregar
  updateLocalStorageCount();
  // --- FIM DA LÓGICA DE CONTAGEM ---


  // --- INÍCIO DA SUA LÓGICA DE FORMULÁRIO (EXISTENTE) ---
  const updateForms = document.querySelectorAll(".form-update-cart");

  updateForms.forEach(form => {
    const qtyInput = form.querySelector(".input-quantity");
    const btnMinus = form.querySelector(".btn-qty-minus");
    const btnPlus = form.querySelector(".btn-qty-plus");

    // Função para submeter o formulário
    const submitForm = () => {
      const cartItem = form.closest('.cart-item');
      if (cartItem) {
        cartItem.classList.add('removing'); 
      }
      form.submit();
    };

    // 1. Clique no Botão de Mais
    btnPlus.addEventListener("click", () => {
      qtyInput.value = parseInt(qtyInput.value, 10) + 1;
      submitForm();
    });

    // 2. Clique no Botão de Menos
    btnMinus.addEventListener("click", () => {
      let currentValue = parseInt(qtyInput.value, 10);
      if (currentValue > 1) {
        qtyInput.value = currentValue - 1;
        submitForm();
      }
    });

    // 3. Mudar manualmente
    qtyInput.addEventListener("change", () => {
      let currentValue = parseInt(qtyInput.value, 10);
      if (currentValue < 1 || isNaN(currentValue)) {
        qtyInput.value = 1; 
      }
      submitForm();
    });
  });
  // --- FIM DA LÓGICA DE FORMULÁRIO ---
});