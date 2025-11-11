function dispatchCartUpdate() {
  window.dispatchEvent(new CustomEvent('cartUpdated'));
  if (window.cartCounter) {
    window.cartCounter.updateCount();
  }
}

async function addToCartWithUpdate(productId, quantity = 1) {
  try {
    const response = await fetch('/api/carrinho/add', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ id_produto: productId, quantidade: quantity })
    });
    
    if (response.ok) {
      dispatchCartUpdate();
      return true;
    }
  } catch (error) {
    console.error('Erro ao adicionar ao carrinho:', error);
  }
  return false;
}