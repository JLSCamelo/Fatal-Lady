document.addEventListener("DOMContentLoaded", function () {
  // --- Elementos do DOM ---
  const productCards = Array.from(document.querySelectorAll(".product-card"));
  const categoryRows = Array.from(document.querySelectorAll(".category-row"));
  const catButtons = Array.from(document.querySelectorAll(".filter-btn"));
  const priceMinInput = document.getElementById("price-min");
  const priceMaxInput = document.getElementById("price-max");
  const priceMinDisplay = document.getElementById("price-min-display");
  const priceMaxDisplay = document.getElementById("price-max-display");
  const colorFiltersContainer = document.getElementById("color-filters");
  const sizeChips = Array.from(document.querySelectorAll(".size-chip"));
  const searchInput = document.getElementById("products-search");
  const clearBtn = document.getElementById("clear-filters");

  // --- Mapeamento de Categoria ---
  // Mapeia o data-filter (numérico) do botão para o data-category (texto) do produto.
  const categoryMap = {};
  catButtons.forEach((btn) => {
    categoryMap[btn.dataset.filter] = btn.textContent.trim();
  });

  // --- Estado dos Filtros ---
  let activeCategory = null;
  const activeColors = new Set();
  const activeSizes = new Set();
  let searchTimeout;

  // --- Inicialização dos Filtros de Preço ---
  const prices = productCards
    .map((c) => parseFloat(c.dataset.price || 0))
    .filter((n) => !isNaN(n));
  const minPrice = prices.length ? Math.floor(Math.min(...prices)) : 0;
  const maxPrice = prices.length ? Math.ceil(Math.max(...prices)) : 1000;

  priceMinInput.min = minPrice;
  priceMinInput.max = maxPrice;
  priceMinInput.value = minPrice;
  priceMaxInput.min = minPrice;
  priceMaxInput.max = maxPrice;
  priceMaxInput.value = maxPrice;

  function formatPrice(value) {
    return Number(value).toLocaleString("pt-BR", {
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
    });
  }

  priceMinDisplay.textContent = formatPrice(priceMinInput.value);
  priceMaxDisplay.textContent = formatPrice(priceMaxInput.value);

  // --- Geração Dinâmica dos Filtros de Cor ---
  const colorSet = new Map();
  productCards.forEach((card) => {
    let color = (card.dataset.color || "Unspecified").trim();
    if (
      color &&
      color.toLowerCase() !== "unspecified" &&
      !colorSet.has(color)
    ) {
      colorSet.set(color, color);
    }
  });

  colorSet.forEach((color, key) => {
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "color-chip";
    btn.dataset.color = key;
    btn.title = key;
    btn.style.backgroundColor = key;
    btn.setAttribute("aria-label", "Filtro cor " + key);
    colorFiltersContainer.appendChild(btn);
  });

  const colorChips = colorFiltersContainer.querySelectorAll(".color-chip");

  // --- Função Principal de Aplicação de Filtros (VERSÃO CORRIGIDA) ---
  function applyFilters() {
    const minVal = parseFloat(priceMinInput.value);
    const maxVal = parseFloat(priceMaxInput.value);
    const searchTerm = (searchInput.value || "").toLowerCase().trim();
    const selectedCategoryName = activeCategory
      ? categoryMap[activeCategory]
      : null;

    productCards.forEach((card) => {
      const cardPrice = parseFloat(card.dataset.price || 0);
      const cardColor = (card.dataset.color || "Unspecified").trim();
      const cardName = (card.dataset.name || "").toLowerCase();
      const cardCategory = (card.dataset.category || "").trim();

      // Lógica de checagem dos outros filtros
      const matchesCategory =
        !selectedCategoryName || cardCategory === selectedCategoryName;
      const matchesPrice = cardPrice >= minVal && cardPrice <= maxVal;
      const matchesColor =
        activeColors.size === 0 || activeColors.has(cardColor);
      const matchesSearch =
        searchTerm.length === 0 || cardName.includes(searchTerm);

      // --- LÓGICA DE TAMANHO CORRIGIDA E ISOLADA ---
      let matchesSize = false;
      if (activeSizes.size === 0) {
        // Se nenhum tamanho for selecionado, todos os produtos passam neste filtro.
        matchesSize = true;
      } else {
        // Pega a string de tamanhos do produto (ex: "39/41/42")
        const productSizesStr = card.dataset.size || "";
        // Verifica se ALGUM dos tamanhos selecionados pelo usuário existe na string do produto.
        // O método .some() para assim que encontra a primeira correspondência.
        matchesSize = [...activeSizes].some((selectedSize) =>
          productSizesStr.split("/").includes(selectedSize)
        );
      }
      // --- FIM DA LÓGICA DE TAMANHO ---

      // A visibilidade final depende de TODOS os filtros serem verdadeiros.
      const isVisible =
        matchesCategory &&
        matchesPrice &&
        matchesColor &&
        matchesSearch &&
        matchesSize;
      card.style.display = isVisible ? "" : "none";
    });

    updateCategoryRowVisibility();
  }

  // --- Funções Auxiliares e de Eventos ---

  function updateCategoryRowVisibility() {
    categoryRows.forEach((row) => {
      const visibleCards = row.querySelector(
        '.product-card:not([style*="display: none"])'
      );
      row.style.display = visibleCards ? "" : "none";
      refreshRowArrows(row);
    });
  }

  function refreshRowArrows(row) {
    const track = row.querySelector(".category-products");
    const prev = row.querySelector(".scroll-prev");
    const next = row.querySelector(".scroll-next");
    if (!track || !prev || !next) return;

    requestAnimationFrame(() => {
      const hasOverflow = track.scrollWidth > track.clientWidth;
      if (!hasOverflow) {
        prev.style.display = "none";
        next.style.display = "none";
        return;
      }
      const maxScroll = Math.max(0, track.scrollWidth - track.clientWidth - 1);
      prev.style.display = track.scrollLeft > 5 ? "inline-flex" : "none";
      next.style.display =
        track.scrollLeft < maxScroll ? "inline-flex" : "none";
    });
  }

  // --- Event Listeners ---

  // Filtros de Categoria (toggle)
  catButtons.forEach((btn) => {
    btn.addEventListener("click", function () {
      const filterValue = this.dataset.filter;
      if (activeCategory === filterValue) {
        activeCategory = null;
        this.classList.remove("active");
      } else {
        activeCategory = filterValue;
        catButtons.forEach((b) => b.classList.remove("active"));
        this.classList.add("active");
      }
      applyFilters();
    });
  });

  // Filtros de Cor (seleção múltipla)
  colorFiltersContainer.addEventListener("click", function (ev) {
    const chip = ev.target.closest(".color-chip");
    if (!chip) return;

    const color = chip.dataset.color;
    if (activeColors.has(color)) {
      activeColors.delete(color);
      chip.classList.remove("active");
    } else {
      activeColors.add(color);
      chip.classList.add("active");
    }
    applyFilters();
  });

  // Filtros de Tamanho (seleção múltipla)
  sizeChips.forEach((chip) => {
    chip.addEventListener("click", function () {
      const size = this.dataset.size;
      if (activeSizes.has(size)) {
        activeSizes.delete(size);
        this.classList.remove("active");
      } else {
        activeSizes.add(size);
        this.classList.add("active");
      }
      applyFilters();
    });
  });

  // Filtro de Preço
  function handlePriceChange() {
    let min = parseFloat(priceMinInput.value);
    let max = parseFloat(priceMaxInput.value);
    if (min > max) {
      [min, max] = [max, min]; // Swap values
    }
    priceMinDisplay.textContent = formatPrice(min);
    priceMaxDisplay.textContent = formatPrice(max);
    applyFilters();
  }
  priceMinInput.addEventListener("input", handlePriceChange);
  priceMaxInput.addEventListener("input", handlePriceChange);

  // Filtro de Busca (com debounce)
  searchInput.addEventListener("input", function () {
    clearTimeout(searchTimeout);
    searchTimeout = setTimeout(applyFilters, 250);
  });

  // Botão de Limpar Filtros
  clearBtn.addEventListener("click", function () {
    // Resetar estados
    activeCategory = null;
    activeColors.clear();
    activeSizes.clear();
    searchInput.value = "";

    // Resetar UI dos filtros
    catButtons.forEach((b) => b.classList.remove("active"));
    colorChips.forEach((c) => c.classList.remove("active"));
    sizeChips.forEach((s) => s.classList.remove("active"));

    // Resetar preço
    priceMinInput.value = priceMinInput.min;
    priceMaxInput.value = priceMaxInput.max;
    priceMinDisplay.textContent = formatPrice(priceMinInput.value);
    priceMaxDisplay.textContent = formatPrice(priceMaxInput.value);

    // Reaplicar filtros (que agora mostrará tudo)
    applyFilters();
  });

  // Navegação por setas nas categorias
  categoryRows.forEach((row) => {
    const track = row.querySelector(".category-products");
    const prev = row.querySelector(".scroll-prev");
    const next = row.querySelector(".scroll-next");
    if (!track || !prev || !next) return;

    let scrollAmount = () => Math.round(track.clientWidth * 0.7);

    prev.addEventListener("click", () => {
      track.scrollBy({ left: -scrollAmount(), behavior: "smooth" });
    });
    next.addEventListener("click", () => {
      track.scrollBy({ left: scrollAmount(), behavior: "smooth" });
    });

    // Usa um observer para performance, em vez de 'scroll' event
    const observer = new IntersectionObserver(() => refreshRowArrows(row), {
      threshold: 0.1,
    });
    observer.observe(row);
    track.addEventListener("scroll", () => refreshRowArrows(row), {
      passive: true,
    });
    window.addEventListener("resize", () => refreshRowArrows(row));
    refreshRowArrows(row);
  });

  // Execução inicial para garantir que o estado da UI esteja correto
  applyFilters();
});
