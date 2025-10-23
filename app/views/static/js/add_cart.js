// quick cart hookup for highlights
document.addEventListener('click', function (e) {
  const btn = e.target.closest && e.target.closest('.add-to-cart');
  if (!btn) return;

  // impedir que, por exemplo, um <a> pai receba clique
  e.preventDefault();

  const card = btn.closest('.highlights-icons');
  if (!card) return;

  const id = card.dataset.id || ('p_' + Math.random().toString(36).slice(2,7));
  const name = card.dataset.name || (card.querySelector('.highlight-name')?.textContent?.trim()) || 'Produto';
  // tentar extrair preço: data-price (preferível) ou texto do elemento
  let price = 0;
  if (card.dataset.price) price = Number(card.dataset.price);
  else {
    const pv = card.querySelector('.price-value')?.textContent || card.querySelector('.highlight-price')?.textContent || '';
    price = Number(String(pv).replace(/[^\d,.\-]/g, '').replace(',', '.')) || 0;
  }

  // depois de calcular id, name, price:
  const imgEl = card.querySelector('img') || card.querySelector('.product-media img');
  const imageSrc = imgEl ? (imgEl.getAttribute('src') || imgEl.src) : null;

  const item = { id, name, price, qty: 1, image: imageSrc };

  if (typeof window.addToCart === 'function') {
    window.addToCart(item);
    // feedback visual rápido
    const oldText = btn.textContent;
    btn.textContent = 'Adicionado ✓';
    btn.setAttribute('aria-disabled', 'true');
    setTimeout(function(){
      btn.textContent = oldText;  
      btn.removeAttribute('aria-disabled');
    }, 900);
  } else {
    console.log('addToCart não encontrado — item:', item);
  }
});
