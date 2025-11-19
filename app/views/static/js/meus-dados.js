document.addEventListener("DOMContentLoaded", () => {
  const btnEdit = document.getElementById("btn-edit");
  const btnCancel = document.getElementById("btn-cancel");
  const formActions = document.getElementById("form-actions");
  const form = document.getElementById("dados-form");
  const inputs = form.querySelectorAll("input, select");

  let originalValues = {};

  inputs.forEach((input) => {
    originalValues[input.name] = input.value;
  });

  btnEdit.addEventListener("click", () => {
    inputs.forEach((input) => {
      input.removeAttribute("readonly");
      input.removeAttribute("disabled");
    });
    formActions.classList.remove("hidden");
    btnEdit.style.display = "none";
  });

  btnCancel.addEventListener("click", () => {
    inputs.forEach((input) => {
      input.value = originalValues[input.name];
      input.setAttribute("readonly", "readonly");
      if (input.tagName === "SELECT") {
        input.setAttribute("disabled", "disabled");
      }
    });
    formActions.classList.add("hidden");
    btnEdit.style.display = "inline-block";
  });

  form.addEventListener("submit", (e) => {
    e.preventDefault();
    alert("Dados atualizados com sucesso!");
    inputs.forEach((input) => {
      originalValues[input.name] = input.value;
      input.setAttribute("readonly", "readonly");
      if (input.tagName === "SELECT") {
        input.setAttribute("disabled", "disabled");
      }
    });
    formActions.classList.add("hidden");
    btnEdit.style.display = "inline-block";
  });
});
