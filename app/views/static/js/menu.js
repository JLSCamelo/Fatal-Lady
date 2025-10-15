// assets/js/menu.js (ATUALIZADO: menu + carrinho simples via localStorage)
document.addEventListener('DOMContentLoaded', function () {
const menuBtn = document.getElementById('menu-hamburguer-icon');
const overlay = document.getElementById('side-overlay');
const closeBtn = document.getElementById('side-close');

if (!menuBtn || !overlay || !closeBtn) {
    console.warn('Menu: elemento(s) essenciais não encontrado(s). Verifique IDs.');
    return;
}

// --- menu open / close ---
function openMenu() {
    overlay.classList.add('open');
    overlay.setAttribute('aria-hidden', 'false');
    document.body.classList.add('no-scroll');
    closeBtn.focus();
    renderCartPreview();
}
function closeMenu() {
    overlay.classList.remove('open');
    overlay.setAttribute('aria-hidden', 'true');
    document.body.classList.remove('no-scroll');
    menuBtn.focus();
}

menuBtn.addEventListener('click', function (e) {
    e.preventDefault();
    overlay.classList.contains('open') ? closeMenu() : openMenu();
});
closeBtn.addEventListener('click', function (e) { e.preventDefault(); closeMenu(); });
overlay.addEventListener('click', function (e) { if (e.target === overlay) closeMenu(); });
document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && overlay.classList.contains('open')) closeMenu(); });

// ----------------- CARRINHO (localStorage simples) -----------------
const CART_KEY = 'cg_cart_v1';
const cartPreviewEl = document.getElementById('cart-preview');
const cartCountEl = document.getElementById('cart-count');
const clearCartBtn = document.getElementById('clear-cart');
const viewCartBtn = document.getElementById('view-cart-btn');
const checkoutBtn = document.getElementById('checkout-btn');

// helpers
function getCart() {
    try {
    const raw = localStorage.getItem(CART_KEY);
    return raw ? JSON.parse(raw) : [];
    } catch (err) { console.error(err); return []; }
}
function saveCart(cart) {
    localStorage.setItem(CART_KEY, JSON.stringify(cart));
    updateCartCount();
}
function updateCartCount() {
    const cart = getCart();
    const totalQty = cart.reduce((s,i)=>s + (i.qty||0), 0);
    if (cartCountEl) cartCountEl.textContent = totalQty;
}

// adicionar item (simples API)
// substitua a implementação atual por esta (menu.js)
window.addToCart = function addToCart(item) {
  // item = { id, name, price, qty (opcional), image (opcional) }
  if (!item || !item.id) return;

  const cart = getCart();
  const idx = cart.findIndex(i => i.id === item.id);

  if (idx > -1) {
    // atualiza quantidade e, se vier image nova, atualiza também
    cart[idx].qty = (cart[idx].qty || 0) + (item.qty || 1);
    if (item.image) cart[idx].image = item.image;
  } else {
    cart.push({
      id: item.id,
      name: item.name || 'Produto',
      price: item.price || 0,
      qty: item.qty || 1,
      image: item.image || null
    });
  }

  saveCart(cart);
  // atualizar preview se estiver aberto
  renderCartPreview();
};

// render do preview
function renderCartPreview() {
    const cart = getCart();
    updateCartCount();

    if (!cartPreviewEl) return;
    cartPreviewEl.innerHTML = '';
    if (cart.length === 0) {
    cartPreviewEl.innerHTML = '<p class="cart-empty">Seu carrinho está vazio.</p>';
    return;
    }

    // criar cada item
    cart.forEach(item => {
    const itemEl = document.createElement('div');
    itemEl.className = 'cart-item';
    itemEl.innerHTML = `
        <div class="thumb" aria-hidden="true">
        ${ item.image ? `<img src="${escapeHtml(item.image)}" alt="${escapeHtml(item.name)}" />` : '' }
        </div>
        <div class="meta">
        <div class="name">${escapeHtml(item.name)}</div>
        <div class="price">R$ ${Number(item.price).toFixed(2)}</div>
        </div>
        <div class="qty" data-id="${item.id}">
        <button class="qty-dec" aria-label="Diminuir">−</button>
        <div class="qty-num">${item.qty}</div>
        <button class="qty-inc" aria-label="Aumentar">+</button>
        <button class="remove-item" aria-label="Remover" style="margin-left:.4rem">✕</button>
        </div>
    `;
    cartPreviewEl.appendChild(itemEl);
    });

    // subtotal / total
    const total = cart.reduce((s,i)=> s + (i.price * (i.qty||1)), 0);
    const totalEl = document.createElement('div');
    totalEl.style.marginTop = '.6rem';
    totalEl.style.fontWeight = 700;
    totalEl.textContent = `Total: R$ ${total.toFixed(2)}`;
    cartPreviewEl.appendChild(totalEl);
}

// manipulação de botões dentro do cart preview (delegation)
cartPreviewEl && cartPreviewEl.addEventListener('click', function (e) {
    const target = e.target;
    const qtyWrap = target.closest('.qty');
    if (!qtyWrap) return;
    const id = qtyWrap.getAttribute('data-id');
    const cart = getCart();
    const idx = cart.findIndex(i=>i.id === id);
    if (idx === -1) return;

    if (target.classList.contains('qty-inc')) {
    cart[idx].qty = (cart[idx].qty || 0) + 1;
    saveCart(cart);
    renderCartPreview();
    return;
    }
    if (target.classList.contains('qty-dec')) {
    cart[idx].qty = Math.max(0, (cart[idx].qty || 0) - 1);
    if (cart[idx].qty === 0) cart.splice(idx,1);
    saveCart(cart);
    renderCartPreview();
    return;
    }
    if (target.classList.contains('remove-item')) {
    cart.splice(idx,1);
    saveCart(cart);
    renderCartPreview();
    return;
    }
});

// limpar carrinho
clearCartBtn && clearCartBtn.addEventListener('click', function (e) {
    e.preventDefault();
    localStorage.removeItem(CART_KEY);
    renderCartPreview();
    updateCartCount();
});

// view cart / checkout (Você pode alterar os hrefs para rotas reais)
viewCartBtn && viewCartBtn.addEventListener('click', function () {
    // abre a página cart.html (padrão). Se você usa SPA, adapte.
    // fechar menu para melhor UX
    closeMenu();
});
checkoutBtn && checkoutBtn.addEventListener('click', function () {
    closeMenu();
});

// inicializar
updateCartCount();

// função utilitária para escapar HTML (segurança)
function escapeHtml(text) {
    if (!text && text !== 0) return '';
    return String(text).replace(/[&<>"']/g, function (m) {
    return ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'})[m];
    });
}

// render quando sidebar abrir (adicionado no openMenu)
// renderCartPreview(); -- já chamado no openMenu

// Exemplo quick-test: se quiser adicionar via console:
// addToCart({ id: 'p1', name:'Produto Teste', price: 49.9, qty:1 });
});
