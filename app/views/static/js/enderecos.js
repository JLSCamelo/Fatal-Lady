function openModal() {
    document.getElementById('modal-endereco').classList.remove('hidden');
    document.getElementById('endereco-form').reset();
    document.getElementById('endereco-id').value = '';
    document.getElementById('modal-title').textContent = 'Novo Endereço';
}

function closeModal() {
    document.getElementById('modal-endereco').classList.add('hidden');
}

function editAddress(id) {
    openModal();
    document.getElementById('modal-title').textContent = 'Editar Endereço';
    document.getElementById('endereco-id').value = id;
}

function setPrincipal(id) {
    if (confirm('Deseja definir este endereço como principal?')) {
        alert('Endereço definido como principal!');
    }
}

function deleteAddress(id) {
    if (confirm('Tem certeza que deseja excluir este endereço?')) {
        alert('Endereço excluído com sucesso!');
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const btnAddAddress = document.getElementById('btn-add-address');
    const btnBuscarCep = document.getElementById('btn-buscar-cep');
    const cepInput = document.getElementById('cep');
    const form = document.getElementById('endereco-form');

    if (btnAddAddress) {
        btnAddAddress.addEventListener('click', openModal);
    }

    if (cepInput) {
        cepInput.addEventListener('input', (e) => {
            let value = e.target.value.replace(/\D/g, '');
            if (value.length > 5) {
                value = value.slice(0, 5) + '-' + value.slice(5, 8);
            }
            e.target.value = value;
        });
    }

    if (btnBuscarCep) {
        btnBuscarCep.addEventListener('click', async () => {
            const cep = cepInput.value.replace(/\D/g, '');
            
            if (cep.length !== 8) {
                alert('CEP inválido!');
                return;
            }

            btnBuscarCep.textContent = 'Buscando...';
            btnBuscarCep.disabled = true;

            try {
                const response = await fetch(`https://viacep.com.br/ws/${cep}/json/`);
                const data = await response.json();

                if (data.erro) {
                    alert('CEP não encontrado!');
                    return;
                }

                document.getElementById('logradouro').value = data.logradouro || '';
                document.getElementById('bairro').value = data.bairro || '';
                document.getElementById('cidade').value = data.localidade || '';
                document.getElementById('estado').value = data.uf || '';
                document.getElementById('numero').focus();
            } catch (error) {
                alert('Erro ao buscar CEP. Tente novamente.');
            } finally {
                btnBuscarCep.textContent = 'Buscar CEP';
                btnBuscarCep.disabled = false;
            }
        });
    }

    if (form) {
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            
            const formData = new FormData(form);
            const data = Object.fromEntries(formData);
            
            console.log('Dados do endereço:', data);
            alert('Endereço salvo com sucesso!');
            closeModal();
        });
    }
});