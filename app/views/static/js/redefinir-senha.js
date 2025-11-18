document.addEventListener("DOMContentLoaded", function () {
  // --- SELETORES ---
  // Use o ID correto do formulário de redefinição
  const form = document.getElementById("reset-form");
  const senhaInput = document.getElementById("senha");
  const confirmarSenhaInput = document.getElementById("confirmar-senha");
  const strengthProgress = document.getElementById("strength-progress");
  const strengthText = document.getElementById("strength-text");
  // Mensagem de erro do HTML
  const errorMessage = document.getElementById("confirm-error");

  // --- 1. LÓGICA DA BARRA DE FORÇA (O seu código, está correto) ---
  if (senhaInput && strengthProgress && strengthText) {
    senhaInput.addEventListener("input", function () {
      const senha = senhaInput.value;
      const strength = calculatePasswordStrength(senha);

      strengthProgress.className = "strength-progress";

      if (senha.length === 0) {
        strengthProgress.style.width = "0%";
        strengthText.textContent = "Força da senha";
        return;
      }

      if (strength < 3) {
        strengthProgress.classList.add("weak");
        strengthText.textContent = "Fraca";
      } else if (strength < 4) {
        strengthProgress.classList.add("medium");
        strengthText.textContent = "Média";
      } else {
        strengthProgress.classList.add("strong");
        strengthText.textContent = "Forte";
      }
    });
  }

  function calculatePasswordStrength(password) {
    let strength = 0;
    if (password.length >= 8) strength++;
    if (password.length >= 12) strength++;
    if (/[a-z]/.test(password) && /[A-Z]/.test(password)) strength++;
    if (/\d/.test(password)) strength++;
    if (/[^a-zA-Z0-9]/.test(password)) strength++;
    return strength;
  }

  // --- 2. LÓGICA DE VALIDAÇÃO NO ENVIO ---
  if (form) {
    form.addEventListener("submit", function (e) {
      // Reseta a mensagem de erro
      errorMessage.style.display = "none";

      const senha = senhaInput.value;
      const confirmarSenha = confirmarSenhaInput.value;

      // Expressões regulares (usadas para a barra de força, mas boas para validação)
      const hasNumber = /\d/;
      const hasSpecialChar = /[^a-zA-Z0-9]/;
      const hasUpper = /[A-Z]/;
      const hasLower = /[a-z]/;

      // Validação de Comprimento Mínimo
      if (senha.length < 8) {
        e.preventDefault(); // Impede o envio
        errorMessage.textContent = "A Senha deve ter no mínimo 8 caracteres!";
        errorMessage.style.display = "block";
        senhaInput.focus();
        return;
      }

      // Validação de regras (ex: número, especial)
      // O medidor de força já indica isso, mas podemos forçar
      if (
        !hasNumber.test(senha) ||
        !hasSpecialChar.test(senha) ||
        !hasLower.test(senha) ||
        !hasUpper.test(senha)
      ) {
        e.preventDefault(); // Impede o envio
        errorMessage.textContent =
          "A senha deve ser 'Forte' (usar maiúsculas, minúsculas, números e símbolos).";
        errorMessage.style.display = "block";
        senhaInput.focus();
        return;
      }

      // Validação de Confirmação de Senha
      if (senha !== confirmarSenha) {
        e.preventDefault(); // Impede o envio
        errorMessage.textContent = "As senhas não coincidem!";
        errorMessage.style.display = "block";
        confirmarSenhaInput.focus();
        return;
      }

      // Se todas as validações passarem, o formulário é enviado
      // (pois o e.preventDefault() não foi chamado)
    });
  }
});
