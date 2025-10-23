// ====== catalogo-filters.js ======
// centraliza filtros: categoria + preço + cores + limpar
document.addEventListener("DOMContentLoaded", function () {
  // elements
  const productCards = Array.from(document.querySelectorAll(".product-card"));
  const categoryRows = Array.from(document.querySelectorAll(".category-row"));
  const catButtons = Array.from(document.querySelectorAll(".filter-btn"));
  const priceMinInput = document.getElementById("price-min");
  const priceMaxInput = document.getElementById("price-max");
  const priceMinDisplay = document.getElementById("price-min-display");
  const priceMaxDisplay = document.getElementById("price-max-display");
  const colorFiltersContainer = document.getElementById("color-filters");
  const clearBtn = document.getElementById("clear-filters");
  const searchInput = document.getElementById("products-search");

  // compute min/max price from DOM products
  const prices = productCards
    .map((c) => parseFloat(c.dataset.price || 0))
    .filter((n) => !isNaN(n));
  const minPrice = prices.length ? Math.min(...prices) : 0;
  const maxPrice = prices.length ? Math.max(...prices) : 1000;

  // init price inputs
  priceMinInput.min = Math.floor(minPrice);
  priceMinInput.max = Math.ceil(maxPrice);
  priceMaxInput.min = Math.floor(minPrice);
  priceMaxInput.max = Math.ceil(maxPrice);

  priceMinInput.value = priceMinInput.min;
  priceMaxInput.value = priceMaxInput.max;

  function fmt(v) {
    return Number(v).toLocaleString("pt-BR", {
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
    });
  }

  priceMinDisplay.textContent = fmt(priceMinInput.value);
  priceMaxDisplay.textContent = fmt(priceMaxInput.value);

  // build unique color list from product data-color attributes
  const colorSet = new Map();
  productCards.forEach((card) => {
    let c = (card.dataset.color || "Unspecified").trim();
    if (!colorSet.has(c)) colorSet.set(c, c);
  });

  // render color chips
  // render color chips (ignora 'Unspecified')
  colorSet.forEach((color, key) => {
    if (!key || key.toLowerCase() === "unspecified") return; // skip fallback values
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "color-chip";
    btn.dataset.color = key;
    btn.title = key;
    // tenta usar como cor; se não for um valor válido, deixa um tom neutro e sem texto
    const isHex = /^#([0-9A-F]{3}){1,2}$/i.test(key.trim());
    if (isHex) {
      btn.style.background = key.trim();
    } else {
      // tenta aplicar nome CSS; se não fizer efeito, usar um background neutro
      btn.style.background = key.toLowerCase();
      if (!btn.style.background) btn.style.background = "#f5f3f1";
    }
    btn.setAttribute("aria-label", "Filtro cor " + key);
    colorFiltersContainer.appendChild(btn);
  });

  // selected states
  let activeCategory = null;
  const activeColors = new Set();

  // helper: apply filters
  function applyFilters() {
    const minVal = parseFloat(priceMinInput.value);
    const maxVal = parseFloat(priceMaxInput.value);
    const search = ((searchInput && searchInput.value) || "")
      .toLowerCase()
      .trim();

    productCards.forEach((card) => {
      const price = parseFloat(card.dataset.price || 0);
      const color = (card.dataset.color || "Unspecified").trim();
      const name = (
        card.dataset.name ||
        card.querySelector(".product-name")?.textContent ||
        ""
      ).toLowerCase();

      const byPrice = price >= minVal && price <= maxVal;
      const byColor = activeColors.size === 0 || activeColors.has(color);
      const bySearch = search.length === 0 || name.includes(search);

      const matches = byPrice && byColor && bySearch;

      // category filter: if active, hide cards not matching category; else within visible rows all cards considered
      if (activeCategory && card.dataset.category !== activeCategory) {
        card.style.display = "none";
      } else {
        card.style.display = matches ? "" : "none";
      }
    });

    // hide/show category rows depending on whether they have visible cards
    categoryRows.forEach((row) => {
      const visibleCards = row.querySelectorAll(
        '.product-card:not([style*="display: none"])'
      );
      if (visibleCards.length === 0) {
        row.style.display = "none";
      } else {
        row.style.display = "";
        refreshRowArrows(row); // recalc arrows for rows that remain visible
      }
    });
  }

  // arrow refresh (independent, safe)
  function refreshRowArrows(row) {
    const track = row.querySelector(".category-products");
    const prev = row.querySelector(".scroll-prev");
    const next = row.querySelector(".scroll-next");
    if (!track || !prev || !next) return;
    requestAnimationFrame(function () {
      const maxScroll = Math.max(0, track.scrollWidth - track.clientWidth - 1);
      prev.style.display = track.scrollLeft > 5 ? "inline-flex" : "none";
      next.style.display =
        track.scrollLeft < maxScroll ? "inline-flex" : "none";
    });
  }

  // init arrows behavior per row (scroll and refresh)
  document.querySelectorAll(".category-row").forEach((row) => {
    const track = row.querySelector(".category-products");
    const prev = row.querySelector(".scroll-prev");
    const next = row.querySelector(".scroll-next");
    if (!track) return;
    let scrollAmount = Math.round(track.clientWidth * 0.7) || 600;
    if (prev)
      prev.addEventListener("click", () => {
        track.scrollBy({ left: -scrollAmount, behavior: "smooth" });
        setTimeout(() => refreshRowArrows(row), 260);
      });
    if (next)
      next.addEventListener("click", () => {
        track.scrollBy({ left: scrollAmount, behavior: "smooth" });
        setTimeout(() => refreshRowArrows(row), 260);
      });
    track.addEventListener("scroll", () => refreshRowArrows(row));
    window.addEventListener("resize", () => {
      scrollAmount = Math.round(track.clientWidth * 0.7) || 600;
      refreshRowArrows(row);
    });
    refreshRowArrows(row);
  });

  // category filter buttons (toggle)
  catButtons.forEach((btn) => {
    btn.addEventListener("click", function () {
      const f = btn.dataset.filter;
      if (activeCategory === f) {
        // toggle off
        activeCategory = null;
        catButtons.forEach((b) => b.classList.remove("active"));
      } else {
        activeCategory = f;
        catButtons.forEach((b) => b.classList.toggle("active", b === btn));
      }
      applyFilters();
    });
  });

  // color chips click
  colorFiltersContainer.addEventListener("click", function (ev) {
    const btn = ev.target.closest(".color-chip");
    if (!btn) return;
    const color = btn.dataset.color;
    if (activeColors.has(color)) {
      activeColors.delete(color);
      btn.classList.remove("active");
    } else {
      activeColors.add(color);
      btn.classList.add("active");
    }
    applyFilters();
  });

  // price inputs events (ensure min <= max)
  function syncPriceInputs() {
    let min = parseFloat(priceMinInput.value);
    let max = parseFloat(priceMaxInput.value);
    if (min > max) {
      // swap to keep valid range
      const t = min;
      min = max;
      max = t;
    }
    priceMinInput.value = min;
    priceMaxInput.value = max;
    priceMinDisplay.textContent = fmt(min);
    priceMaxDisplay.textContent = fmt(max);
    applyFilters();
  }
  priceMinInput.addEventListener("input", syncPriceInputs);
  priceMaxInput.addEventListener("input", syncPriceInputs);

  // search
  if (searchInput) {
    let timeout;
    searchInput.addEventListener("input", function () {
      clearTimeout(timeout);
      timeout = setTimeout(() => applyFilters(), 220);
    });
  }

  // clear btn
  clearBtn.addEventListener("click", function () {
    // reset category
    activeCategory = null;
    catButtons.forEach((b) => b.classList.remove("active"));
    // reset color chips
    activeColors.clear();
    colorFiltersContainer
      .querySelectorAll(".color-chip")
      .forEach((c) => c.classList.remove("active"));
    // reset price
    priceMinInput.value = priceMinInput.min;
    priceMaxInput.value = priceMaxInput.max;
    priceMinDisplay.textContent = fmt(priceMinInput.value);
    priceMaxDisplay.textContent = fmt(priceMaxInput.value);
    // reset search
    if (searchInput) searchInput.value = "";
    // show all
    productCards.forEach((c) => (c.style.display = ""));
    categoryRows.forEach((r) => (r.style.display = ""));
    // refresh arrows
    categoryRows.forEach(refreshRowArrows);
  });

  // initial apply to ensure UI consistent
  applyFilters();
});
