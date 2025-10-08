// assets/js/nav-enhancements.js
// Corrige posicionamento para que HEADER + NAV fiquem juntos e visíveis (sobrepostos ao topo).
// Mantém badge do carrinho e busca.
// Incluir com defer (já está assim no index.html).

document.addEventListener('DOMContentLoaded', function () {
  const CART_KEY = 'cg_cart_v1';
  const $ = s => document.querySelector(s);
  const $$ = s => Array.from(document.querySelectorAll(s));
  const debounce = (fn, t=100)=>{ let h; return (...a)=>{ clearTimeout(h); h=setTimeout(()=>fn(...a), t); }; };

  // localizar o elemento do menu/hamburguer
  const menuIcon = document.getElementById('menu-hamburguer-icon') || document.querySelector('[data-menu], .menu-toggle, .menu-hamburger');
  let nav = null;
  if (menuIcon) nav = menuIcon.closest('nav') || (menuIcon.closest('header') && menuIcon.closest('header').querySelector('nav')) || null;
  if (!nav) nav = $('nav[role="navigation"]') || $('nav') || null;
  if (!nav) {
    console.warn('nav-enhancements: <nav> não encontrado. Abortando.');
    return;
  }

  // localizar um header que esteja ANTES do nav no fluxo visual/DOM (o header que você espera ver)
  // buscamos um <header> que esteja acima do nav na ordem do DOM e que tenha altura visível > 0
  let headerEl = document.querySelector('header');
  if (headerEl) {
    // garantir que header aparece antes do nav no DOM (source order)
    const bodyChildren = Array.from(document.body.children);
    const headerIndex = bodyChildren.indexOf(headerEl);
    const navIndex = bodyChildren.indexOf(nav);
    if (headerIndex === -1 || navIndex === -1 || headerIndex > navIndex) {
      // header global não precede nav diretamente — tentar previousElementSibling
      const prev = nav.previousElementSibling;
      if (prev && prev.tagName && prev.tagName.toLowerCase() === 'header') headerEl = prev;
      else headerEl = null;
    }
  }

  // se nav está DENTRO de um header, tratamos o header como contêiner
  if (!headerEl && nav.closest('header')) {
    headerEl = nav.closest('header');
  }

  // criar placeholder (se ainda não existir)
  let placeholder = document.querySelector('.nav-placeholder');
  if (!placeholder) {
    placeholder = document.createElement('div');
    placeholder.className = 'nav-placeholder';
    nav.parentNode.insertBefore(placeholder, nav.nextSibling);
  }

  function fixHeaderAndNav() {
  // limpa ajustes anteriores
  try {
    if (headerEl) {
      headerEl.style.position = '';
      headerEl.style.top = '';
      headerEl.style.left = '';
      headerEl.style.right = '';
      headerEl.style.zIndex = '';
      headerEl.style.width = '';
    }
    nav.style.position = '';
    nav.style.top = '';
    nav.style.left = '';
    nav.style.right = '';
    nav.style.zIndex = '';
    nav.style.width = '';
    nav.style.transform = '';
  } catch (e) {}

  // força layout e mede
  const navRect = nav.getBoundingClientRect();
  let headerRect = { height: 0 };
  if (headerEl && headerEl !== nav) headerRect = headerEl.getBoundingClientRect();
  const headerIsParent = headerEl && headerEl.contains(nav);

  // alturas inteiras (usar round para reduzir subpixel surprises)
  const headerHeight = headerIsParent ? 0 : Math.round(headerRect.height || 0);
  const navHeight = Math.round(navRect.height || 0);

  // se existirem header separado + nav, fixamos ambos e "nudge" o nav 1px pra cima via transform
  if (headerEl && !headerIsParent) {
    // fixa header
    headerEl.style.position = 'fixed';
    headerEl.style.top = '0px';
    headerEl.style.left = '0px';
    headerEl.style.right = '0px';
    headerEl.style.width = '100%';
    headerEl.style.zIndex = '1000';

    // fixa nav logo abaixo do header, e aplica um nudge visual de -1px com transform
    nav.style.position = 'fixed';
    nav.style.top = headerHeight + 'px';
    nav.style.left = '0px';
    nav.style.right = '0px';
    nav.style.width = '100%';
    nav.style.zIndex = '1000';
    nav.style.transform = 'translateY(-1px)'; // corrige o gap por subpixel
  } else {
    // nav dentro do header ou sem header: fixa o container único
    const target = headerEl && headerEl.contains(nav) ? headerEl : nav;
    target.style.position = 'fixed';
    target.style.top = '0px';
    target.style.left = '0px';
    target.style.right = '0px';
    target.style.width = '100%';
    target.style.zIndex = '1000';
    // não aplicamos transform neste caso
  }

  // placeholder: reserva o espaço visual total (height soma) MAS desconta 1px
  const totalHeight = (headerEl && !headerIsParent ? headerHeight + navHeight : (headerIsParent ? Math.round(headerRect.height || navHeight) : navHeight)) || 68;
  const placeholderHeight = Math.max(0, totalHeight - 1); // desconta 1px (nudge)
  placeholder.style.height = placeholderHeight + 'px';
  document.documentElement.style.setProperty('--site-nav-height', totalHeight + 'px');

  // se precisar recalcular logo depois (fontes/imagens), refaz pequeno delay
  setTimeout(function () {
    // mantém transform (nudge) — motivo: evita novo subpixel gap
    // mas garante placeholder coerente (evita saltos)
  }, 40);
}


  // executar inicialmente (pequeno timeout para esperar imagens e fontes)
  setTimeout(fixHeaderAndNav, 60);

  // recalcular no resize (debounced)
  window.addEventListener('resize', debounce(fixHeaderAndNav, 120));

  // também observar mudanças no header/nav (ex.: classes que alteram altura)
  try {
    const mo = new MutationObserver(debounce(fixHeaderAndNav, 120));
    mo.observe(nav, { attributes: true, subtree: false, attributeFilter: ['class', 'style'] });
    if (headerEl && headerEl !== nav) mo.observe(headerEl, { attributes: true, subtree: false, attributeFilter: ['class', 'style'] });
  } catch (e) { /* se MutationObserver não disponível, não é crítico */ }

  // ------- restante: cart badge, open overlay e search (mantive as funcionalidades) -------

  // localizar cart button (mantendo heurística)
  let cartBtn = document.getElementById('shopping-kart-icon') || document.getElementById('cart-icon') || document.querySelector('.icon-cart') || document.querySelector('.cart-icon') || document.getElementById('cart-btn');
  if (!cartBtn) {
    const near = menuIcon ? (menuIcon.parentElement || document.body) : document.body;
    cartBtn = Array.from(near.querySelectorAll('img,button,a,svg')).find(el => {
      const id = (el.id || '').toLowerCase();
      const cls = (el.className || '').toLowerCase();
      const alt = (el.getAttribute && (el.getAttribute('alt') || '')).toLowerCase();
      return id.includes('cart') || cls.includes('cart') || alt.includes('carrinho') || alt.includes('cart');
    });
  }
  if (!cartBtn) {
    cartBtn = document.createElement('button');
    cartBtn.type = 'button';
    cartBtn.id = 'shopping-kart-icon';
    cartBtn.className = 'cart-created';
    cartBtn.setAttribute('aria-label', 'Abrir carrinho');
    cartBtn.innerHTML = '<img src="assets/img/home/icons-main/carrinho-de-compras.png" alt="Carrinho" />';
    nav.appendChild(cartBtn);
  }

  // badge
  let badge = document.getElementById('cart-count-badge');
  if (!badge) {
    badge = document.createElement('span');
    badge.id = 'cart-count-badge';
    badge.setAttribute('aria-live', 'polite');
    if (cartBtn.parentNode) cartBtn.parentNode.insertBefore(badge, cartBtn.nextSibling);
    else cartBtn.appendChild(badge);
  }

  function readCart() {
  try {
    const raw = localStorage.getItem(CART_KEY);
    return raw ? JSON.parse(raw) : [];
  } catch (e) { return []; }
}
function computeCartCount() {
  return readCart().reduce((s,i)=> s + (Number(i.qty)||0), 0);
}
function updateBadge(animate=true) {
  if (!badge) return;
  const n = computeCartCount();
  badge.textContent = String(n);
  if (animate) {
    badge.style.transform = 'scale(1.1)';
    badge.style.transition = 'transform .12s ease';
    setTimeout(()=> badge.style.transform = '', 150);
  }
}

// Atualiza no carregamento
updateBadge(false);

// Atualiza quando usar addToCart
if (typeof window.addToCart === 'function') {
  const orig = window.addToCart.bind(window);
  window.addToCart = function (item) {
    const res = orig(item);
    setTimeout(()=> updateBadge(true), 80);
    return res;
  };
}

// Atualiza quando qualquer outra aba alterar o carrinho
window.addEventListener('storage', function (e) {
  if (e.key === CART_KEY) updateBadge(true);
});

// Atualiza se algum script sobrescrever o localStorage (evento custom)
window.addEventListener('localStorageSet', function (e) {
  if (e && e.detail && String(e.detail.key) === CART_KEY) updateBadge(true);
});

// Fallback: sincroniza a cada 2 segundos (garantia absoluta)
setInterval(()=> updateBadge(false), 2000);
  if (typeof window.addToCart === 'function') {
    const orig = window.addToCart.bind(window);
    window.addToCart = function (item) {
      const res = orig(item);
      setTimeout(()=> updateBadge(true), 80);
      return res;
    };
  }

  window.addEventListener('storage', function (e) { if (e.key === CART_KEY) updateBadge(true); });
  window.addEventListener('localStorageSet', function (e) { if (e && e.detail && String(e.detail.key) === CART_KEY) updateBadge(true); });

  // abrir sidebar ao clicar no cart
  const overlay = document.getElementById('side-overlay');
  const closeBtn = document.getElementById('side-close');
  cartBtn.addEventListener('click', function (ev) {
    ev.preventDefault();
    if (overlay) {
      overlay.classList.add('open');
      overlay.setAttribute('aria-hidden','false');
      document.body.classList.add('no-scroll');
      if (closeBtn) closeBtn.focus();
      try { if (typeof window.renderCartPreview === 'function') window.renderCartPreview(); } catch(e){}
    } else {
      window.location.href = 'cart.html';
    }
  });

  // última garantia: recalc e badge após carregamento completo
  window.addEventListener('load', function () { setTimeout(fixHeaderAndNav, 80); setTimeout(updateBadge, 80); });
});
