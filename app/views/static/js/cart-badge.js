// Arquivo: /static/js/cart-badge.js
// DEVE SER CARREGADO EM TODAS AS PÁGINAS

document.addEventListener("DOMContentLoaded", () => {
  const updateBadgeVisibility = () => {
    // 1. CHECAGEM DE AUTENTICAÇÃO (Sem alteração)
    const body = document.querySelector("body");
    const isAuthenticated = body
      ? body.dataset.isAuthenticated === "true"
      : false;

    // Lógica para usuários DESLOGADOS
    if (!isAuthenticated) {
      localStorage.removeItem("cartItemCount"); // Limpa o storage

      const existingBadge = document.querySelector(".cart-badge");
      if (existingBadge) {
        // Se estiver deslogado, ESCONDEMOS o badge.
        existingBadge.classList.add("hidden");
      }
      return;
    }

    // --- INÍCIO DA NOVA LÓGICA (LOGADO) ---

    // 2. ENCONTRAR O WRAPPER (Sem alteração)
    const cartWrapper = document.querySelector(".cart-link-wrapper");
    if (!cartWrapper) return;

    // 3. LÓGICA DO "TRANCO" (Leitura de Valor)
    let itemCount;
    const storedCount = localStorage.getItem("cartItemCount"); // Valor preciso (com quantidades)

    if (storedCount !== null) {
      // Se já visitou o carrinho, usa o valor preciso do localStorage
      itemCount = parseInt(storedCount, 10);
    } else {
      // NOVO: Se NUNCA visitou o carrinho (pós-login), usa o valor injetado no HTML
      //
      const initialCount = body
        ? parseInt(body.dataset.cartCount || "0", 10)
        : 0;
      itemCount = initialCount;

      // Salva esse valor inicial no localStorage para não precisar ler o HTML de novo
      localStorage.setItem("cartItemCount", itemCount);
    }

    // 4. LÓGICA "SEMPRE VISÍVEL" (Criação/Atualização)

    let badge = cartWrapper.querySelector(".cart-badge");

    // Se o badge não existir, CRIE-O (mesmo se for 0)
    if (!badge) {
      badge = document.createElement("span");
      badge.className = "cart-badge";
      cartWrapper.appendChild(badge);
    }

    // Define o texto (Ex: "0" ou "5")
    badge.textContent = itemCount;

    // Garante que NUNCA esteja escondido se o usuário estiver LOGADO
    badge.classList.remove("hidden");
  };

  // Inicializa o badge na carga da página
  updateBadgeVisibility();

  // Ouve eventos de atualização (de outras abas ou do carrinho.js)
  window.addEventListener("storage", updateBadgeVisibility);
  window.addEventListener("cartUpdated", updateBadgeVisibility);
});
