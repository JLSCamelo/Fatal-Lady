// static/js/excluir-conta.js
(function () {
  document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("delete-confirm-form");
    if (!form) return;

    const cpfInput = document.getElementById("cpf");
    const birthInput = document.getElementById("data_nascimento");
    const passwordInput = document.getElementById("senha");
    const submitBtn = form.querySelector('button[type="submit"]');
    const globalErrorEl = document.getElementById("form-global-error");

    if (!cpfInput || !birthInput || !passwordInput || !submitBtn) return;

    // Máscara de CPF
    cpfInput.addEventListener("input", () => {
      const current = cpfInput.value;
      cpfInput.value = maskCpf(current);
      clearFieldError(cpfInput);
      hideGlobalError();
    });

    birthInput.addEventListener("input", () => {
      clearFieldError(birthInput);
      hideGlobalError();
    });

    passwordInput.addEventListener("input", () => {
      clearFieldError(passwordInput);
      hideGlobalError();
    });

    cpfInput.addEventListener("blur", () => validateCpfField(cpfInput));
    birthInput.addEventListener("blur", () => validateBirthField(birthInput));
    passwordInput.addEventListener("blur", () =>
      validatePasswordField(passwordInput)
    );

    form.addEventListener("submit", (event) => {
      event.preventDefault();
      clearAllErrors();

      const cpfOk = validateCpfField(cpfInput);
      const birthOk = validateBirthField(birthInput);
      const passwordOk = validatePasswordField(passwordInput);

      if (!cpfOk || !birthOk || !passwordOk) {
        showGlobalError("Por favor, corrija os campos destacados.");
        return;
      }

      // Tudo ok -> envia normalmente
      submitBtn.disabled = true;
      const originalText = submitBtn.textContent;
      submitBtn.textContent = "Confirmando...";

      form.submit(); // deixa o backend tratar token, etc.

      // Se o backend fizer redirect sem recarregar JS, esse trecho nem chega a rodar depois.
      setTimeout(() => {
        submitBtn.disabled = false;
        submitBtn.textContent = originalText;
      }, 5000);
    });

    // ========= Helpers de erro =========

    function clearAllErrors() {
      [cpfInput, birthInput, passwordInput].forEach((input) =>
        clearFieldError(input)
      );
      hideGlobalError();
    }

    function clearFieldError(input) {
      input.classList.remove("input-error");
      const group = input.closest(".form-group");
      if (!group) return;
      const err = group.querySelector(".field-error");
      if (err) err.remove();
    }

    function setFieldError(input, message) {
      input.classList.add("input-error");
      const group = input.closest(".form-group");
      if (!group) return;

      let err = group.querySelector(".field-error");
      if (!err) {
        err = document.createElement("p");
        err.className = "field-error";
        group.appendChild(err);
      }
      err.textContent = message;
    }

    function showGlobalError(message) {
      if (!globalErrorEl) return;
      globalErrorEl.textContent = message;
      globalErrorEl.hidden = false;
    }

    function hideGlobalError() {
      if (!globalErrorEl) return;
      globalErrorEl.hidden = true;
      globalErrorEl.textContent = "";
    }

    // ========= Validações =========

    function validateCpfField(input) {
      const raw = input.value || "";
      const digits = raw.replace(/\D/g, "");

      if (!digits) {
        setFieldError(input, "Informe seu CPF.");
        return false;
      }

      if (!isValidCpf(digits)) {
        setFieldError(input, "CPF inválido. Verifique os números digitados.");
        return false;
      }

      clearFieldError(input);
      return true;
    }

    function validateBirthField(input) {
      const value = input.value;

      if (!value) {
        setFieldError(input, "Informe sua data de nascimento.");
        return false;
      }

      const today = new Date();
      const birthDate = new Date(value + "T00:00:00");

      if (Number.isNaN(birthDate.getTime())) {
        setFieldError(input, "Data de nascimento inválida.");
        return false;
      }

      if (birthDate > today) {
        setFieldError(
          input,
          "A data de nascimento não pode ser uma data futura."
        );
        return false;
      }

      // Opcional: checar idade mínima (ex: 16 anos)
      const minAge = 16;
      const cutoff = new Date(
        today.getFullYear() - minAge,
        today.getMonth(),
        today.getDate()
      );
      if (birthDate > cutoff) {
        setFieldError(
          input,
          `É necessário ter pelo menos ${minAge} anos para concluir esta ação.`
        );
        return false;
      }

      clearFieldError(input);
      return true;
    }

    function validatePasswordField(input) {
      const value = input.value || "";

      if (!value) {
        setFieldError(input, "Informe sua senha atual.");
        return false;
      }

      if (value.length < 6) {
        setFieldError(
          input,
          "Senha muito curta. Informe pelo menos 6 caracteres."
        );
        return false;
      }

      clearFieldError(input);
      return true;
    }

    // ========= Utilitários =========

    function maskCpf(value) {
      const digits = value.replace(/\D/g, "").slice(0, 11);
      const len = digits.length;

      if (len <= 3) return digits;
      if (len <= 6) return digits.replace(/(\d{3})(\d{1,3})/, "$1.$2");
      if (len <= 9)
        return digits.replace(/(\d{3})(\d{3})(\d{1,3})/, "$1.$2.$3");
      return digits.replace(
        /(\d{3})(\d{3})(\d{3})(\d{1,2})/,
        "$1.$2.$3-$4"
      );
    }

    function isValidCpf(digits) {
      // 11 dígitos numéricos
      if (!/^\d{11}$/.test(digits)) return false;

      // Rejeita CPFs com todos os dígitos iguais
      if (/^(\d)\1{10}$/.test(digits)) return false;

      // Validação dos dígitos verificadores
      const calcCheck = (base) => {
        let sum = 0;
        for (let i = 0; i < base.length; i++) {
          sum += parseInt(base.charAt(i), 10) * (base.length + 1 - i);
        }
        const mod = (sum * 10) % 11;
        return mod === 10 ? 0 : mod;
      };

      const d1 = calcCheck(digits.slice(0, 9));
      const d2 = calcCheck(digits.slice(0, 10));

      return d1 === parseInt(digits.charAt(9), 10) &&
        d2 === parseInt(digits.charAt(10), 10)
        ? true
        : false;
    }
  });
})();
