// Arquivo seguro - evita inicializar comportamentos antigos do Swiper na seção "collections".
// Mantém o restante do site intacto.

document.addEventListener('DOMContentLoaded', () => {
    try {
        // Se a página tiver um contêiner .swiper (outros usos), NÃO forçamos inicialização aqui.
        // Nosso banner usa a classe .banner-marquee e funciona via CSS puro.
        // Mantemos esse arquivo inofensivo para evitar quebras.
        const maybeSwiper = document.querySelector('.swiper');
        if (maybeSwiper) {
        // Não inicializamos Swiper automaticamente aqui.
        // Se você quiser inicializar outras instâncias do Swiper em outras seções,
        // recomendo criar um init específico e seguro apenas para essas seções.
        // Para debug:
        // console.log('Swiper detected on page but init disabled in assets/js/swiper.js (safe mode).');
        }
    } catch (err) {
        console.error('Erro seguro no swiper.js (não fatal):', err);
    }
});
