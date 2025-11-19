// === CONFIG ===
// Ajuste a rota se for outra
const DELETE_ENDPOINT = "/excluir/conta";

document.addEventListener("DOMContentLoaded", () => {
  const btn = document.getElementById("btn-danger");
  if (!btn) return;

  btn.addEventListener("click", openDeleteModal);
});

// =========================
// 1. ABRIR MODAL BONITO
// =========================
function openDeleteModal(event) {
  event.preventDefault();

  let overlay = document.getElementById("delete-modal-overlay");
  if (!overlay) overlay = buildModal();

  overlay.classList.add("visible");
}

// =========================
// 2. CRIAR MODAL
// =========================
function buildModal() {
  const overlay = document.createElement("div");
  overlay.id = "delete-modal-overlay";
  overlay.className = "delete-modal-overlay";

  const modal = document.createElement("div");
  modal.className = "delete-modal";

  modal.innerHTML = `
        <div class="delete-modal-icon">!</div>
        <h2 class="delete-modal-title">Excluir conta</h2>

        <p class="delete-modal-text">
            Enviaremos um e-mail com o link para confirmar a exclusão.
            Esta ação só será concluída após você confirmar pelo e-mail.
        </p>

        <div class="delete-modal-actions">
            <button class="delete-btn cancel">Cancelar</button>
            <button class="delete-btn confirm">Confirmar</button>
        </div>
    `;

  overlay.appendChild(modal);
  document.body.appendChild(overlay);

  // Eventos
  overlay
    .querySelector(".cancel")
    .addEventListener("click", () => closeModal());
  overlay.addEventListener("click", (ev) => {
    if (ev.target === overlay) closeModal();
  });

  overlay.querySelector(".confirm").addEventListener("click", () => {
    handleDelete(overlay);
  });

  return overlay;
}

// =========================
// 3. FECHAR MODAL
// =========================
function closeModal() {
  const overlay = document.getElementById("delete-modal-overlay");
  if (!overlay) return;
  overlay.classList.remove("visible");
}

// ===========================================
// 4. CHAMAR BACKEND E DISPARAR POP-UP BONITO
// ===========================================
async function handleDelete(overlay) {
  const confirmBtn = overlay.querySelector(".confirm");
  const cancelBtn = overlay.querySelector(".cancel");

  confirmBtn.disabled = true;
  cancelBtn.disabled = true;
  confirmBtn.textContent = "Enviando...";

  try {
    const resposta = await fetch(DELETE_ENDPOINT, {
      method: "POST",
      credentials: "include",
    });

    if (resposta.ok) {
      closeModal();
      showToast(
        "success",
        "Enviamos um e-mail com instruções para concluir a exclusão da conta."
      );
      return;
    }

    const erro = await resposta.json();
    showToast("error", erro.detail || "Erro inesperado ao solicitar exclusão.");

    confirmBtn.disabled = false;
    cancelBtn.disabled = false;
    confirmBtn.textContent = "Confirmar";
  } catch (err) {
    console.error(err);
    showToast("error", "Erro ao se conectar ao servidor.");
    confirmBtn.disabled = false;
    cancelBtn.disabled = false;
    confirmBtn.textContent = "Confirmar";
  }
}

// =========================
// 5. SISTEMA DE TOAST
// =========================
function ensureToastContainer() {
  let c = document.getElementById("status-toast-container");
  if (!c) {
    c = document.createElement("div");
    c.id = "status-toast-container";
    document.body.appendChild(c);
  }
  return c;
}

function showToast(type, text) {
  const container = ensureToastContainer();

  const toast = document.createElement("div");
  toast.className = `status-toast ${type === "success" ? "success" : "error"}`;

  toast.innerHTML = `
        <div class="status-toast__icon">${type === "success" ? "✓" : "!"}</div>
        <div class="status-toast__content">
            <strong class="status-toast__title">${
              type === "success" ? "Tudo certo!" : "Erro"
            }</strong>
            <p class="status-toast__message">${text}</p>
        </div>
        <button class="status-toast__close">×</button>
    `;

  toast.querySelector(".status-toast__close").onclick = () => hideToast(toast);

  container.appendChild(toast);

  requestAnimationFrame(() => toast.classList.add("is-visible"));
  setTimeout(() => hideToast(toast), type === "success" ? 4000 : 5000);
}

function hideToast(t) {
  if (!t) return;
  t.classList.remove("is-visible");
  t.addEventListener("transitionend", () => t.remove(), { once: true });
}
