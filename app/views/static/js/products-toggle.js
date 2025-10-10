// assets/js/products-toggle.js
document.addEventListener('DOMContentLoaded', function () {
  const grid = document.getElementById('products-grid');
  const btn  = document.getElementById('load-more');
  if (!grid || !btn) return;

  let collapsed = true;
  let initTimeout = null;

  // debounce util
  function debounce(fn, wait = 120) {
    let t;
    return function () { clearTimeout(t); t = setTimeout(fn, wait); };
  }

  // calcula a altura visível correspondente à PRIMEIRA LINHA de cards (considera apenas elementos visíveis)
  function computeFirstRowHeight() {
    const cards = Array.from(grid.querySelectorAll('.product-card')).filter(c => c.offsetParent !== null);
    if (!cards.length) return 0;

    const firstTop = cards[0].offsetTop;
    const firstRowCards = cards.filter(c => c.offsetTop === firstTop);
    // usar boundingClientRect para calcular bottom relativo ao grid top
    const bottoms = firstRowCards.map(c => c.getBoundingClientRect().bottom);
    const gridTop = grid.getBoundingClientRect().top;
    const visibleHeight = Math.max(...bottoms) - gridTop + 8; // +8px de folga
    return Math.ceil(visibleHeight);
  }

  function collapseGrid() {
    const h = computeFirstRowHeight() || 0;
    if (h <= 0) {
      // sem altura calculada, não colapsa
      grid.style.maxHeight = 'none';
      grid.classList.remove('collapsed');
      grid.classList.add('expanded');
      btn.style.display = 'none';
      collapsed = false;
      return;
    }
    grid.style.maxHeight = h + 'px';
    grid.classList.add('collapsed');
    grid.classList.remove('expanded');
    btn.textContent = 'Ver mais';
    btn.setAttribute('aria-expanded', 'false');
    collapsed = true;
  }

  function expandGrid() {
    // primeiro define maxHeight pro scrollHeight para animar
    grid.style.maxHeight = grid.scrollHeight + 'px';
    grid.classList.remove('collapsed');
    grid.classList.add('expanded');
    btn.textContent = 'Ver menos';
    btn.setAttribute('aria-expanded', 'true');
    collapsed = false;
    // após a transição, remove maxHeight para deixar o grid responsivo
    setTimeout(function () {
      if (!collapsed) grid.style.maxHeight = 'none';
    }, 420);
  }

  // decide se devemos mostrar o botão (se houver mais itens que a primeira linha)
  function evaluateNeedButton() {
    const cards = Array.from(grid.querySelectorAll('.product-card')).filter(c => c.offsetParent !== null);
    if (cards.length === 0) {
      btn.style.display = 'none';
      grid.style.maxHeight = 'none';
      return;
    }
    const firstTop = cards[0].offsetTop;
    const firstRowCount = cards.filter(c => c.offsetTop === firstTop).length;
    if (cards.length <= firstRowCount) {
      btn.style.display = 'none';
      grid.style.maxHeight = 'none';
      collapsed = false;
      grid.classList.remove('collapsed');
      grid.classList.add('expanded');
    } else {
      btn.style.display = '';
      // se estivermos no estado inicial, manter colapsado
      if (collapsed) collapseGrid();
    }
  }

  // init (espera um pouco por imagens/carregamento)
  function init() {
    evaluateNeedButton();
  }

  // botão
  btn.addEventListener('click', function (e) {
    e.preventDefault();
    if (collapsed) {
      expandGrid();
      // rolagem suave para manter contexto (opcional)
      btn.scrollIntoView({ behavior: 'smooth', block: 'center' });
    } else {
      collapseGrid();
      // quando recolher, rolar para topo da sessão para o usuário ver início
      const section = grid.closest('.products-section') || grid;
      section.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  });

  // recalcula quando muda o tamanho da janela
  window.addEventListener('resize', debounce(function () {
    // recomputar: se está colapsado, recoloca a altura; se expandido, garante "none"
    if (collapsed) collapseGrid(); else grid.style.maxHeight = 'none';
  }, 150));

  // observar mudanças no grid (ex.: filtros que escondem cards)
  const mo = new MutationObserver(debounce(function () {
    evaluateNeedButton();
  }, 120));
  mo.observe(grid, { childList: true, subtree: true, attributes: true, attributeFilter: ['style', 'class'] });

  // chamar init após layout estabilizar (pequeno delay para imagens)
  initTimeout = setTimeout(init, 80);
});
