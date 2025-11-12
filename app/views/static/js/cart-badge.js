document.addEventListener("DOMContentLoaded", () => {
  
  const updateBadgeVisibility = () => {
    const cartWrapper = document.querySelector(".cart-link-wrapper");
    if (!cartWrapper) return; 

    // Lê o total salvo no localStorage
    const itemCount = parseInt(localStorage.getItem("cartItemCount") || "0", 10);

    let badge = cartWrapper.querySelector(".cart-badge");

    // Se o total for 0, esconde ou remove o badge
    if (itemCount === 0) {
      if (badge) {
        badge.classList.add("hidden"); // Usa a classe do seu CSS
      }
      return; 
    }

    // Se for > 0 e o badge não existir, crie-o
    if (!badge) {
      badge = document.createElement("span");
      badge.className = "cart-badge"; // Classe do 'cart-badge.css'
      cartWrapper.appendChild(badge);
    }

    // Atualiza o total e garante que está visível
    badge.textContent = itemCount;
    badge.classList.remove("hidden");
  };

  // 1. Atualiza no carregamento inicial da página
  updateBadgeVisibility();

  // 2. Ouve por atualizações de outras abas
  window.addEventListener('storage', (event) => {
    if (event.key === 'cartItemCount') {
      updateBadgeVisibility();
    }
  });

  // 3. Ouve o evento customizado do 'carrinho.js'
  window.addEventListener('cartUpdated', () => {
    updateBadgeVisibility();
  });
});