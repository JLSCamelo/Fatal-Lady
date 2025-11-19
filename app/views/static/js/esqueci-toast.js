// static/js/esqueci-toast.js
(function () {
  document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector(".register-form");
    if (!form) return;

    const submitBtn = form.querySelector('button[type="submit"]');
    const originalBtnText = submitBtn ? submitBtn.textContent : null;

    form.addEventListener("submit", async (event) => {
      event.preventDefault();

      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.textContent = "Enviando...";
      }

      try {
        const formData = new FormData(form);

        const response = await fetch(form.action || "/esqueci-senha-login", {
          method: form.method || "POST",
          body: formData,
          headers: {
            "X-Requested-With": "XMLHttpRequest",
            Accept: "application/json",
          },
        });

        const contentType = response.headers.get("Content-Type") || "";
        let data = null;

        if (contentType.includes("application/json")) {
          try {
            data = await response.json();
          } catch (_) {
            data = null;
          }
        } else {
          data = {};
        }

        const success = response.ok;

        const backendMessage =
          (data && (data.message || data.detail || data.error)) || null;

        const finalMessage =
          backendMessage ||
          (success
            ? "Se o e-mail informado estiver cadastrado, você receberá o link para redefinição."
            : "Não foi possível enviar o e-mail de redefinição.");

        showStatusToast(success ? "success" : "error", finalMessage);

        if (success) {
          form.reset();
        }
      } catch (err) {
        console.error("[esqueci-toast] erro na requisição:", err);
        showStatusToast(
          "error",
          "Erro ao se conectar com o servidor. Verifique sua conexão e tente novamente."
        );
      } finally {
        if (submitBtn) {
          submitBtn.disabled = false;
          submitBtn.textContent =
            originalBtnText || "Enviar Link de Redefinição";
        }
      }
    });

    // ========= Helpers de Toast =========

    function ensureToastContainer() {
      let container = document.getElementById("status-toast-container");
      if (!container) {
        container = document.createElement("div");
        container.id = "status-toast-container";
        document.body.appendChild(container);
      }
      return container;
    }

    function showStatusToast(type, text) {
      const container = ensureToastContainer();

      const toast = document.createElement("div");
      toast.className =
        "status-toast " + (type === "success" ? "success" : "error");

      const icon = document.createElement("div");
      icon.className = "status-toast__icon";
      icon.textContent = type === "success" ? "✓" : "!";

      const content = document.createElement("div");
      content.className = "status-toast__content";

      const title = document.createElement("strong");
      title.className = "status-toast__title";
      title.textContent =
        type === "success" ? "Tudo certo!" : "Algo deu errado";

      const message = document.createElement("p");
      message.className = "status-toast__message";
      message.textContent = text || "";

      content.appendChild(title);
      content.appendChild(message);

      const closeBtn = document.createElement("button");
      closeBtn.type = "button";
      closeBtn.className = "status-toast__close";
      closeBtn.setAttribute("aria-label", "Fechar aviso");
      closeBtn.textContent = "×";

      closeBtn.addEventListener("click", () => hideToast(toast));

      toast.appendChild(icon);
      toast.appendChild(content);
      toast.appendChild(closeBtn);

      container.appendChild(toast);

      // animação de entrada
      requestAnimationFrame(() => {
        toast.classList.add("is-visible");
      });

      // auto-hide (sucesso mais rápido, erro um pouco mais longo)
      const timeout = type === "success" ? 4000 : 5000;
      setTimeout(() => hideToast(toast), timeout);
    }

    function hideToast(toast) {
      if (!toast) return;
      toast.classList.remove("is-visible");
      toast.addEventListener(
        "transitionend",
        () => {
          try {
            toast.remove();
          } catch (_) {}
        },
        { once: true }
      );
    }
  });
})();
