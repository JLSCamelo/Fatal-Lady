const modal = document.getElementById("modal-endereco");
const form = document.getElementById("endereco-form");

function openModal(address = null) {
  if (!modal || !form) return;

  const title = document.getElementById("modal-title");
  const principalCheckbox = document.getElementById("principal");

  form.reset();
  form.querySelector("#endereco-id").value = "";
  principalCheckbox.checked = false;

  if (address) {
    title.textContent = "Editar Endereço";
    form.querySelector("#endereco-id").value = address.id;
    form.querySelector("#apelido").value = address.apelido || "";
    form.querySelector("#destinatario").value = address.destinatario || "";
    form.querySelector("#cep").value = address.cep || "";
    form.querySelector("#logradouro").value = address.rua || "";
    form.querySelector("#numero").value = address.numero || "";
    form.querySelector("#complemento").value = address.complemento || "";
    form.querySelector("#bairro").value = address.bairro || "";
    form.querySelector("#cidade").value = address.cidade || "";
    form.querySelector("#estado").value = address.estado || "";
    principalCheckbox.checked = Boolean(address.principal === "true" || address.principal === true);
  } else {
    title.textContent = "Novo Endereço";
  }

  modal.classList.remove("hidden");
}

function closeModal() {
  if (!modal || !form) return;
  form.reset();
  form.querySelector("#endereco-id").value = "";
  modal.classList.add("hidden");
}

function editAddress(id) {
  const card = document.querySelector(`.endereco-card[data-id="${id}"]`);
  if (!card) return;

  const address = {
    id,
    apelido: card.dataset.apelido,
    destinatario: card.dataset.destinatario,
    cep: card.dataset.cep,
    rua: card.dataset.rua,
    numero: card.dataset.numero,
    complemento: card.dataset.complemento,
    bairro: card.dataset.bairro,
    cidade: card.dataset.cidade,
    estado: card.dataset.estado,
    principal: card.dataset.principal,
  };

  openModal(address);
}

async function deleteAddress(id) {
  if (!confirm("Deseja realmente excluir este endereço?")) return;

  const response = await fetch(`/me/enderecos/${id}/deletar`, { method: "DELETE" });
  if (!response.ok) {
    alert("Não foi possível excluir o endereço.");
    return;
  }

  window.location.reload();
}

async function setPrincipal(id) {
  const response = await fetch(`/me/enderecos/${id}/principal`, {
    method: "PATCH",
  });

  if (!response.ok) {
    alert("Não foi possível definir o endereço como principal.");
    return;
  }

  window.location.reload();
}

if (typeof window !== "undefined") {
  window.openModal = openModal;
  window.closeModal = closeModal;
  window.editAddress = editAddress;
  window.deleteAddress = deleteAddress;
  window.setPrincipal = setPrincipal;
}

document.addEventListener("DOMContentLoaded", () => {
  const addButton = document.getElementById("btn-add-address");
  if (addButton) {
    addButton.addEventListener("click", () => openModal());
  }
});