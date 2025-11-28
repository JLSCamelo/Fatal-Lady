document.addEventListener("DOMContentLoaded", () => {
  const btnEdit = document.getElementById("btn-edit");
  const btnCancel = document.getElementById("btn-cancel");
  const formActions = document.getElementById("form-actions");
  const form = document.getElementById("dados-form");
  const inputs = form ? form.querySelectorAll("input, select") : [];

  let originalValues = {};

  inputs.forEach((input) => {
    originalValues[input.name] = input.value;
  });

  function setReadOnly(state) {
    inputs.forEach((input) => {
      if (state) {
        input.setAttribute("readonly", "readonly");
        if (input.tagName === "SELECT") {
          input.setAttribute("disabled", "disabled");
        }
      } else {
        input.removeAttribute("readonly");
        if (input.tagName === "SELECT") {
          input.removeAttribute("disabled");
        }
      }
    });
  };

  if (btnEdit) {
    btnEdit.addEventListener("click", () => {
      setReadOnly(false);
      formActions.classList.remove("hidden");
      btnEdit.style.display = "none";

    });
  }

  if (btnCancel) {
    btnCancel.addEventListener("click", () => {
      inputs.forEach((input) => {
        input.value = originalValues[input.name];
      });
      setReadOnly(true);
      formActions.classList.add("hidden");
      if (btnEdit) btnEdit.style.display = "inline-block";
    });
  }

  if (form) {
    form.addEventListener("submit", async (e) => {
      e.preventDefault();

      const formData = new FormData(form);

      try {
        const response = await fetch(form.action, {
          method: "POST",
          body: formData,
        });

        if (response.redirected) {
          window.location.href = response.url;
          return;
        }

        if (!response.ok) {
          const contentType = response.headers.get("content-type") || "";
          const error = contentType.includes("application/json")
            ? await response.json()
            : { detail: response.statusText };
          throw new Error(error.detail || "Erro ao salvar os dados.");
        }

        const data = await response.json();
        alert(data.mensagem || "Dados atualizados com sucesso!");

        if (data.usuario) {
          Object.entries(data.usuario).forEach(([key, value]) => {
            if (key in originalValues && form[key]) {
              form[key].value = value || "";
            }
          });
        }

        inputs.forEach((input) => {
          originalValues[input.name] = input.value;
        });

        setReadOnly(true);
        formActions.classList.add("hidden");
        if (btnEdit) btnEdit.style.display = "inline-block";
      } catch (error) {
        console.error(error);
        alert(error.message);
      }
    });
  }
});

