// Toggle password visibility (sem alteração funcional além de aria-pressed atualizada)
      document.getElementById("toggle-password").addEventListener("click", function () {
        const passwordInput = document.getElementById("senha");
        const eyeIcon = this.querySelector(".eye-icon");
        const eyeOffIcon = this.querySelector(".eye-off-icon");
        const pressed = this.getAttribute("aria-pressed") === "true";

        if (!pressed) {
          passwordInput.type = "text";
          eyeIcon.style.display = "none";
          eyeOffIcon.style.display = "block";
          this.setAttribute("aria-label", "Ocultar senha");
          this.setAttribute("aria-pressed", "true");
        } else {
          passwordInput.type = "password";
          eyeIcon.style.display = "block";
          eyeOffIcon.style.display = "none";
          this.setAttribute("aria-label", "Mostrar senha");
          this.setAttribute("aria-pressed", "false");
        }
      });