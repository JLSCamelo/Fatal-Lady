// products UI: busca, filtros e ligação do botão add-to-cart
document.addEventListener('DOMContentLoaded', function () {
  const grid = document.getElementById('products-grid');
  const searchInput = document.getElementById('products-search');
  const filterBtns = document.querySelectorAll('.filter-btn');
  const loadMoreBtn = document.getElementById('load-more');

  if (!grid) return;

  // filtro por categoria (data-filter)
  filterBtns.forEach(btn => {
    btn.addEventListener('click', function () {
      filterBtns.forEach(b=>{ b.classList.remove('active'); b.setAttribute('aria-selected','false'); });
      this.classList.add('active'); this.setAttribute('aria-selected','true');
      const filter = this.dataset.filter;
      applyFilters(filter, searchInput?.value || '');
    });
  });

  // busca
  if (searchInput) {
    let t;
    searchInput.addEventListener('input', function () {
      clearTimeout(t);
      t = setTimeout(()=> {
        const filterBtn = document.querySelector('.filter-btn.active');
        const currentFilter = filterBtn?.dataset?.filter || 'all';
        applyFilters(currentFilter, this.value);
      }, 180);
    });
  }

  function applyFilters(category = 'all', q = '') {
    q = String(q || '').trim().toLowerCase();
    const cards = Array.from(grid.querySelectorAll('.product-card'));
    cards.forEach(card => {
      const name = String(card.dataset.name || card.querySelector('.product-name')?.textContent || '').toLowerCase();
      const cat = String(card.dataset.category || '').toLowerCase();
      const matchesCategory = (category === 'all') ? true : (cat === category);
      const matchesSearch = q === '' ? true : (name.indexOf(q) !== -1 || (card.dataset.id || '').toLowerCase().indexOf(q) !== -1);
      if (matchesCategory && matchesSearch) {
        card.style.display = ''; // mostra
      } else {
        card.style.display = 'none'; // esconde
      }
    });
  }

  // load more (se quiser carregar mais via JS; aqui apenas scroll para próximos itens)
  if (loadMoreBtn) {
    loadMoreBtn.addEventListener('click', function () {
      // comportamento simples: rolar mais pra baixo (pode virar fetch para API)
      window.scrollBy({ top: 400, left: 0, behavior: 'smooth' });
    });
  }

  // ligar botões add-to-cart automaticamente (usa window.addToCart / fallback console)
  document.addEventListener('click', function (e) {
    const btn = e.target.closest && e.target.closest('.add-to-cart');
    if (!btn) return;
    e.preventDefault();

    const card = btn.closest('.product-card');
    if (!card) return;
    const id = card.dataset.id || ('p_' + Math.random().toString(36).slice(2,7));
    const name = card.dataset.name || (card.querySelector('.product-name')?.textContent?.trim()) || 'Produto';
    const price = Number(card.dataset.price || card.querySelector('.price-value')?.textContent?.replace(/[^\d,.\-]/g,'').replace(',','.') || 0) || 0;
<<<<<<< HEAD
    
    // --- dentro do listener onde já obtém card, id, name, price ---
    const imgEl = card.querySelector('.product-media img') || card.querySelector('img');
    const imageSrc = imgEl ? (imgEl.getAttribute('src') || imgEl.src) : null;

    const item = { id, name, price, qty: 1, image: imageSrc };
=======

    const item = { id, name, price, qty: 1 };
>>>>>>> 45833ccc4ef94b15890ebafc0aa288548945ec6e
    if (typeof window.addToCart === 'function') {
      window.addToCart(item);
      // feedback visual
      const old = btn.innerHTML;
      btn.innerHTML = 'Adicionado ✓';
      btn.disabled = true;
      setTimeout(()=> { btn.innerHTML = old; btn.disabled = false; }, 900);
    } else {
      console.log('addToCart não encontrado — item:', item);
    }
<<<<<<< HEAD

=======
>>>>>>> 45833ccc4ef94b15890ebafc0aa288548945ec6e
  });
});

// dentro de applyFilters(), após esconder/mostrar os cards:
document.dispatchEvent(new CustomEvent('productsFiltered'));
