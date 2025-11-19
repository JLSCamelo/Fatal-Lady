// static/js/login-enhance.js
(function () {
  document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector(".login-form");
    if (!form) return;

    const emailInput = form.querySelector("#email");
    const passwordInput = form.querySelector("#senha");
    const passwordWrapper = form.querySelector(".password-wrapper");
    const submitBtn = form.querySelector('button[type="submit"]');
    const originalBtnText = submitBtn ? submitBtn.textContent : null;

    if (!emailInput || !passwordInput) return;

    // -------- Helpers de erro no campo --------
    function clearPasswordError() {
      passwordInput.classList.remove("is-invalid");
      if (passwordWrapper) passwordWrapper.classList.remove("shake");

      const msg = form.querySelector(".field-error-message");
      if (msg) msg.remove();
    }

    function showPasswordError(message) {
      const text = message || "Usuário ou senha incorretos.";

      clearPasswordError();
      passwordInput.classList.add("is-invalid");

      if (passwordWrapper) {
        passwordWrapper.classList.add("shake");
        setTimeout(() => {
          passwordWrapper.classList.remove("shake");
        }, 300);
      }

      passwordInput.value = "";
      passwordInput.focus();

      const errorEl = document.createElement("p");
      errorEl.className = "field-error-message";
      errorEl.textContent = text;
      const row =
        passwordInput.closest(".input-row") || passwordInput.parentElement;
      if (row) row.appendChild(errorEl);

      showInlineToast("error", text);
    }

    // -------- Helpers de toast (reaproveitando CSS existente) --------
    function ensureToastContainer() {
      let container = document.getElementById("pop-up-container");
      if (!container) {
        container = document.createElement("div");
        container.id = "pop-up-container";
        document.body.appendChild(container);
      }
      return container;
    }

    function showInlineToast(type, text) {
      const container = ensureToastContainer();
      const toast = document.createElement("div");
      toast.className = "toast " + (type === "error" ? "error" : "");

      const textNode = document.createElement("div");
      textNode.className = "text";
      textNode.textContent = text || "";

      const closeBtn = document.createElement("button");
      closeBtn.className = "close";
      closeBtn.type = "button";
      closeBtn.innerText = "✕";
      closeBtn.addEventListener("click", () => {
        toast.classList.remove("show");
        setTimeout(() => {
          try {
            toast.remove();
          } catch (e) {}
        }, 300);
      });

      toast.appendChild(textNode);
      toast.appendChild(closeBtn);
      container.appendChild(toast);

      // animação de entrada
      requestAnimationFrame(() => toast.classList.add("show"));

      // auto-hide
      setTimeout(() => {
        toast.classList.remove("show");
        setTimeout(() => {
          try {
            toast.remove();
          } catch (e) {}
        }, 300);
      }, 3500);
    }

    // Limpa estado de erro enquanto o usuário digita
    passwordInput.addEventListener("input", clearPasswordError);

    // -------- Intercepta submit --------
    form.addEventListener("submit", async (event) => {
      event.preventDefault();
      clearPasswordError();

      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.textContent = "Entrando...";
      }

      try {
        const formData = new FormData(form);

        const response = await fetch(form.action || "/login", {
          method: form.method || "POST",
          body: formData,
          headers: {
            "X-Requested-With": "XMLHttpRequest",
            Accept: "application/json",
          },
          redirect: "follow",
        });

        // Se redirecionou para algo que não é /login, tratamos como sucesso
        if (response.redirected && !response.url.includes("/login")) {
          window.location.href = response.url;
          return;
        }

        const contentType = response.headers.get("Content-Type") || "";
        if (contentType.includes("application/json")) {
          let data = null;
          try {
            data = await response.json();
          } catch (_) {
            data = null;
          }

          if (data) {
            if (data.ok === false || data.error === "invalid_credentials") {
              showPasswordError(data.message);
              return;
            }

            if (data.redirect_to) {
              window.location.href = data.redirect_to;
              return;
            }
          }
        }

        // Se status 400/401, assume credenciais inválidas
        if (
          !response.ok &&
          (response.status === 400 || response.status === 401)
        ) {
          showPasswordError();
          return;
        }

        // Fallback: se continuou em /login, assume erro
        if (!response.redirected || response.url.includes("/login")) {
          showPasswordError();
          return;
        }

        // Último fallback: redireciona
        window.location.href = response.url;
      } catch (err) {
        console.error("[login-enhance] erro no login:", err);
        showInlineToast(
          "error",
          "Erro ao se conectar com o servidor. Tente novamente em instantes."
        );
      } finally {
        if (submitBtn) {
          submitBtn.disabled = false;
          submitBtn.textContent = originalBtnText || "Entrar";
        }
      }
    });
  });
})();
