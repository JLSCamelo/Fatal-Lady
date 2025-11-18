document.addEventListener('DOMContentLoaded', function() {
  const hero = document.getElementById('hero');
  const heroContent = document.querySelector('.hero-content');
  const heroScrollIndicator = document.querySelector('.hero-scroll-indicator');
  const heroOverlay = document.querySelector('.hero-overlay');
  const nav = document.getElementById('main_nav');

  let lastScrollY = 0;
  const heroHeight = hero ? hero.offsetHeight : 0;

  function handleScroll() {
    const currentScroll = window.pageYOffset;

    if (hero && heroContent && heroScrollIndicator && heroOverlay) {
      const scrollPercent = Math.min(currentScroll / (heroHeight * 0.5), 1);

      const contentOpacity = 1 - scrollPercent;
      heroContent.style.opacity = contentOpacity;
      heroScrollIndicator.style.opacity = contentOpacity;

      heroOverlay.style.opacity = 0.6 + scrollPercent * 0.3;
      heroOverlay.style.transform = `scale(${1 + scrollPercent * 0.05})`;
    }

    lastScrollY = currentScroll;
  }

  window.addEventListener('scroll', handleScroll);
  handleScroll();

  let ticking = false;
  window.addEventListener("scroll", function () {
    if (!ticking) {
      window.requestAnimationFrame(function () {
        handleScroll();
        ticking = false;
      });
      ticking = true;
    }
  });

  const observerOptions = {
    threshold: 0.12,
    rootMargin: "0px 0px -60px 0px",
  };

  const fadeInObserver = new IntersectionObserver(function (entries) {
    entries.forEach((entry, index) => {
      if (entry.isIntersecting) {
        setTimeout(() => {
          entry.target.style.opacity = "1";
          entry.target.style.transform = "translateY(0)";
        }, index * 60);
        fadeInObserver.unobserve(entry.target);
      }
    });
  }, observerOptions);

  const animatedElements = document.querySelectorAll(
    ".benefit-item, .featured-card, .category-card, .testimonial-card, .faq-item, .stat-item, .newsletter-card"
  );

  animatedElements.forEach((el) => {
    el.style.opacity = "0";
    el.style.transform = "translateY(25px)";
    el.style.transition =
      "opacity 0.7s cubic-bezier(0.4, 0, 0.2, 1), transform 0.7s cubic-bezier(0.4, 0, 0.2, 1)";
    fadeInObserver.observe(el);
  });

  // Função de 'easing' para aceleração e desaceleração suave
  function easeInOutCubic(t, b, c, d) {
    t /= d / 2;
    if (t < 1) return (c / 2) * t * t * t + b;
    t -= 2;
    return (c / 2) * (t * t * t + 2) + b;
  }

  // Função de rolagem personalizada
  function customSmoothScroll(targetPosition, duration) {
    const startPosition = window.pageYOffset;
    const distance = targetPosition - startPosition;
    let startTime = null;

    function animation(currentTime) {
      if (startTime === null) startTime = currentTime;
      const timeElapsed = currentTime - startTime;
      const run = easeInOutCubic(
        timeElapsed,
        startPosition,
        distance,
        duration
      );
      window.scrollTo(0, run);
      if (timeElapsed < duration) requestAnimationFrame(animation);
    }

    requestAnimationFrame(animation);
  }

  const heroScrollIndicatorEl = document.querySelector(
    ".hero-scroll-indicator"
  );
  if (heroScrollIndicatorEl) {
    heroScrollIndicatorEl.addEventListener("click", function () {
      const benefitsSection = document.getElementById("benefits-bar");
      if (benefitsSection) {
        // Posição alvo (com 80px de offset para a navbar)
        const targetPosition = benefitsSection.offsetTop - 80;

        // Duração da rolagem em milissegundos (aqui está o controle de "lenta")
        const scrollDuration = 1200; // 1.2 segundos. Aumente se quiser mais lento.

        // Chama a nova função em vez do window.scrollTo
        customSmoothScroll(targetPosition, scrollDuration);
      }
    });
  }

  const faqLabels = document.querySelectorAll(".faq-item label");
  faqLabels.forEach((label) => {
    label.addEventListener("click", function () {
      const input = this.previousElementSibling;
      if (input && input.type === "checkbox") {
        setTimeout(() => {
          if (input.checked) {
            this.closest(".faq-item").scrollIntoView({
              behavior: "smooth",
              block: "nearest",
            });
          }
        }, 150);
      }
    });
  });

  const carouselNewsletter = document.querySelector(".carousel-newsletter");
  if (carouselNewsletter) {
    let isDown = false;
    let startX;
    let scrollLeft;

    carouselNewsletter.addEventListener("mousedown", (e) => {
      isDown = true;
      carouselNewsletter.style.cursor = "grabbing";
      startX = e.pageX - carouselNewsletter.offsetLeft;
      scrollLeft = carouselNewsletter.scrollLeft;
    });

    carouselNewsletter.addEventListener("mouseleave", () => {
      isDown = false;
      carouselNewsletter.style.cursor = "grab";
    });

    carouselNewsletter.addEventListener("mouseup", () => {
      isDown = false;
      carouselNewsletter.style.cursor = "grab";
    });

    carouselNewsletter.addEventListener("mousemove", (e) => {
      if (!isDown) return;
      e.preventDefault();
      const x = e.pageX - carouselNewsletter.offsetLeft;
      const walk = (x - startX) * 2;
      carouselNewsletter.scrollLeft = scrollLeft - walk;
    });

    carouselNewsletter.style.cursor = "grab";
  }

  const newsletterButtons = document.querySelectorAll(".newsletter-cta-btn");
  newsletterButtons.forEach((btn) => {
    btn.addEventListener("click", function (e) {
      e.preventDefault();
      const originalText = this.textContent;
      this.textContent = "Processando...";
      this.disabled = true;

      setTimeout(() => {
        this.textContent = "✓ Cadastrado!";
        setTimeout(() => {
          this.textContent = originalText;
          this.disabled = false;
        }, 2000);
      }, 1200);
    });
  });

  const allHoverElements = document.querySelectorAll(
    ".hero-cta, .btn-outline, .featured-card, .category-card, .testimonial-card"
  );

  allHoverElements.forEach((el) => {
    el.addEventListener("mouseenter", function () {
      this.style.transition = "all 0.35s cubic-bezier(0.4, 0, 0.2, 1)";
    });
  });

  const benefitItems = document.querySelectorAll(".benefit-item");
  benefitItems.forEach((item, index) => {
    setTimeout(() => {
      item.style.animation = `slideInUp 0.6s ease forwards`;
    }, index * 100);
  });

  const featuredCards = document.querySelectorAll(".featured-card");
  featuredCards.forEach((card, index) => {
    card.style.animationDelay = `${index * 0.1}s`;
  });

  const style = document.createElement("style");
  style.textContent = `
    @keyframes slideInUp {
      from {
        opacity: 0;
        transform: translateY(30px);
      }
      to {
        opacity: 1;
        transform: translateY(0);
      }
    }
  `;
  document.head.appendChild(style);

  handleScroll();

  window.addEventListener("load", function () {
    document.body.style.opacity = "1";
  });

  const sizeTableRows = document.querySelectorAll(".size-table tbody tr");
  sizeTableRows.forEach((row) => {
    row.addEventListener("click", function () {
      sizeTableRows.forEach((r) => (r.style.background = ""));
      this.style.background = "rgba(203, 19, 19, 0.08)";
      this.style.transition = "background 0.3s ease";
    });
  });

  const parallaxElements = document.querySelectorAll(
    ".story-image img, .category-image img"
  );
  window.addEventListener("scroll", function () {
    const scrolled = window.pageYOffset;
    parallaxElements.forEach((el) => {
      const rect = el.getBoundingClientRect();
      if (rect.top < window.innerHeight && rect.bottom > 0) {
        const speed = 0.3;
        const yPos = -(scrolled * speed);
        el.style.transform = `translateY(${yPos * 0.05}px)`;
      }
    });
  });

  const testimonialCards = document.querySelectorAll(".testimonial-card");
  testimonialCards.forEach((card, index) => {
    card.style.transitionDelay = `${index * 0.1}s`;
  });

  const categoryCards = document.querySelectorAll(".category-card");
  let categoryIndex = 0;
  const categoryInterval = setInterval(() => {
    if (categoryIndex < categoryCards.length) {
      categoryCards[categoryIndex].style.transform = "scale(1.05)";
      setTimeout(() => {
        categoryCards[categoryIndex].style.transform = "scale(1)";
      }, 300);
      categoryIndex++;
    } else {
      clearInterval(categoryInterval);
    }
  }, 200);

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("in-view");
        }
      });
    },
    {
      threshold: 0.1,
    }
  );

  document.querySelectorAll("section").forEach((section) => {
    observer.observe(section);
  });

  const statsObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          const statItems = entry.target.querySelectorAll(".stat-item strong");
          statItems.forEach((stat) => {
            const finalValue = parseInt(stat.textContent);
            let currentValue = 0;
            const increment = finalValue / 50;
            const timer = setInterval(() => {
              currentValue += increment;
              if (currentValue >= finalValue) {
                stat.textContent =
                  finalValue + (stat.textContent.includes("+") ? "+" : "%");
                clearInterval(timer);
              } else {
                stat.textContent =
                  Math.floor(currentValue) +
                  (stat.textContent.includes("+") ? "+" : "%");
              }
            }, 30);
          });
          statsObserver.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.5 }
  );

  const storyStats = document.querySelector(".story-stats");
  if (storyStats) {
    statsObserver.observe(storyStats);
  }
});
