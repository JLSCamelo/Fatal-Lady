document.addEventListener("DOMContentLoaded", () => {
  try {
    const el = document.querySelector("#banner-fade");
    if (!el) return;

    const banner = new Swiper("#banner-fade", {
      effect: "fade", // efeito fade suave
      fadeEffect: { crossFade: true }, // crossfade suave entre slides
      slidesPerView: 1,
      centeredSlides: true,
      loop: true, // loop infinito
      speed: 800, // duração da transição (ms)
      autoplay: {
        delay: 4000, // tempo de exibição de cada slide
        disableOnInteraction: false,
        pauseOnMouseEnter: true,
      },
      preloadImages: true,
      lazy: false,
      navigation: false, // sem setas
      pagination: false, // sem bolinhas
      a11y: {
        enabled: true,
      },
      // medidas de estabilidade
      observer: true,
      observeParents: true,
      observeSlideChildren: true,
    });

    // update on resize to avoid visual glitches
    window.addEventListener("resize", () => {
      try {
        banner.update();
      } catch (e) {
        /* noop */
      }
    });
  } catch (err) {
    console.error("Erro ao inicializar banner-fade:", err);
  }
});
