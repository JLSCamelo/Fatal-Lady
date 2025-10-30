// nav_enchancements.js - versão final simplificada
document.addEventListener('DOMContentLoaded', function () {
  const CART_KEY = 'cg_cart_v1';

  let cartBtn = document.getElementById('kart-icon');
  if (!cartBtn) return;

  let badge = document.getElementById('cart-count-badge');
  if (!badge) {
    badge = document.createElement('span');
    badge.id = 'cart-count-badge';
    badge.setAttribute('aria-live', 'polite');
    badge.style.cssText = 'position:absolute;top:-8px;right:-8px;background:#cb1313;color:#fff;border-radius:50%;width:20px;height:20px;display:flex;align-items:center;justify-content:center;font-size:0.75rem;font-weight:700;box-shadow:0 2px 4px rgba(0,0,0,0.2);';
    
    const wrapper = document.createElement('div');
    wrapper.style.position = 'relative';
    wrapper.style.display = 'inline-block';
    cartBtn.parentNode.insertBefore(wrapper, cartBtn);
    wrapper.appendChild(cartBtn);
    wrapper.appendChild(badge);
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
    const n = computeCartCount();
    badge.textContent = String(n);
    badge.style.display = n > 0 ? 'flex' : 'none';
    if (animate && n > 0) {
      badge.style.transform = 'scale(1.2)';
      badge.style.transition = 'transform 0.15s ease';
      setTimeout(()=> badge.style.transform = 'scale(1)', 150);
    }
  }

  updateBadge(false);

  if (typeof window.addToCart === 'function') {
    const orig = window.addToCart.bind(window);
    window.addToCart = function (item) {
      const res = orig(item);
      setTimeout(()=> updateBadge(true), 80);
      return res;
    };
  }

  window.addEventListener('storage', function (e) {
    if (e.key === CART_KEY) updateBadge(true);
  });

  window.addEventListener('localStorageSet', function (e) {
    if (e && e.detail && String(e.detail.key) === CART_KEY) updateBadge(true);
  });

  setInterval(()=> updateBadge(false), 2000);
});