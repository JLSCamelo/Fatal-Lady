document.addEventListener('DOMContentLoaded', function () {
  const messages = [
    '<b>Frete Grátis</b> para Compras Acima de R$ 299,00',
    '<b>5% OFF</b> no pagamento via Pix',
    '<b>10% OFF</b> na sua primeira compra',
    'Parcele em até <b>10x sem juros</b>'
  ];

  const promoText = document.getElementById('promo-text');
  if (!promoText) return;

  let idx = 0;
  const intervalMs = 5000; // tempo visível de cada mensagem

  function nextMessage() {
    // fade out
    promoText.classList.add('is-hidden');
    setTimeout(() => {
      // troca o conteúdo (usa innerHTML para manter <b>)
      idx = (idx + 1) % messages.length;
      promoText.innerHTML = messages[idx];
      // fade in
      promoText.classList.remove('is-hidden');
    }, 360); // deve combinar com o transition do CSS (~350ms)
  }

  // inicia o ciclo depois de um tempo inicial para que usuário veja a primeira
  setInterval(nextMessage, intervalMs);
});