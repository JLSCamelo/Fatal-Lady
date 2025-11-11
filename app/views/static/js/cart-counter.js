// /static/js/cart-counter.js (versão híbrida)
class CartCounter {
  constructor(badgeId = 'cart-badge') {
    this.badge = document.getElementById(badgeId);
    this.init();
  }

  init() {
    if (!this.badge) {
      console.error('Badge element not found');
      return;
    }
    this.updateCount();
    this.listenToStorage();
  }

  async fetchCartCount() {
    try {
      const response = await fetch('/api/carrinho/count', {
        credentials: 'include'
      });
      if (response.ok) {
        const data = await response.json();
        return data.count || 0;
      }
    } catch (error) {
      console.warn('API indisponível:', error);
    }
    return 0;
  }

  async updateCount() {
    const count = await this.fetchCartCount();
    this.setCount(count);
  }

  setCount(count) {
    if (!this.badge) return;
    
    this.badge.textContent = count > 99 ? '99+' : count;
    
    if (count === 0) {
      this.badge.classList.add('hidden');
    } else {
      this.badge.classList.remove('hidden');
      this.badge.classList.add('pulse');
      setTimeout(() => this.badge.classList.remove('pulse'), 300);
    }
  }

  listenToStorage() {
    window.addEventListener('cartUpdated', () => {
      this.updateCount();
    });
    
    setInterval(() => {
      this.updateCount();
    }, 5000);
  }
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => {
    window.cartCounter = new CartCounter();
  });
} else {
  window.cartCounter = new CartCounter();
}