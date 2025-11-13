// Arquivo: /static/js/cart-badge.js
// DEVE SER CARREGADO EM TODAS AS PÁGINAS

document.addEventListener("DOMContentLoaded", () => {
  
  const updateBadgeVisibility = () => {
    
    // 1. CHECAGEM DE AUTENTICAÇÃO: Leitura do <body>
    const body = document.querySelector("body");
    // Se o elemento <body> não for encontrado (impossível em HTML válido) ou o atributo for "false",
    // assumimos que o usuário está deslogado.
    const isAuthenticated = body ? body.dataset.isAuthenticated === "true" : false;

    // Lógica para usuários DESLOGADOS
    if (!isAuthenticated) {
      // 1.1 Limpa o localStorage (resolve o problema da contagem fantasma)
      localStorage.removeItem("cartItemCount");
      
      // 1.2 Garante que o badge esteja escondido
      const existingBadge = document.querySelector(".cart-badge");
      if (existingBadge) {
        existingBadge.classList.add("hidden");
      }
      return; // Interrompe a exibição do badge para deslogados
    }

    // Lógica para usuários LOGADOS (continua)
    const cartWrapper = document.querySelector(".cart-link-wrapper");
    // Se a estrutura HTML não estiver correta, para aqui.
    if (!cartWrapper) return; 

    // 2. LÊ O VALOR
    // Se 'cartItemCount' foi limpo ao deslogar, agora será "null", e o fallback "0" será usado.
    const itemCount = parseInt(localStorage.getItem("cartItemCount") || "0", 10);

    let badge = cartWrapper.querySelector(".cart-badge");

    // 3. DECISÃO: MOSTRAR OU ESCONDER
    if (itemCount === 0) {
      if (badge) {
        badge.classList.add("hidden"); 
      }
      return; 
    }

    // 4. CRIAÇÃO/ATUALIZAÇÃO DO BADGE
    if (!badge) {
      badge = document.createElement("span");
      badge.className = "cart-badge"; 
      cartWrapper.appendChild(badge);
    }

    badge.textContent = itemCount;
    badge.classList.remove("hidden");
  };

  // Inicializa o badge na carga da página
  updateBadgeVisibility();

  // Ouve eventos de atualização (de outras abas ou do carrinho.js)
  window.addEventListener('storage', updateBadgeVisibility);
  window.addEventListener('cartUpdated', updateBadgeVisibility);
});