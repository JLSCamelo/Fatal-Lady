document.addEventListener('DOMContentLoaded', function() {
  const form = document.getElementById('register-form');
  const senhaInput = document.getElementById('senha');
  const confirmarSenhaInput = document.getElementById('confirmar-senha');
  const cepInput = document.getElementById('cep');
  const telefoneInput = document.getElementById('telefone');
  const strengthProgress = document.getElementById('strength-progress');
  const strengthText = document.getElementById('strength-text');

  if (senhaInput && strengthProgress && strengthText) {
    senhaInput.addEventListener('input', function() {
      const senha = senhaInput.value;
      const strength = calculatePasswordStrength(senha);
      
      strengthProgress.className = 'strength-progress';
      
      if (senha.length === 0) {
        strengthProgress.style.width = '0%';
        strengthText.textContent = 'Força da senha';
        return;
      }
      
      if (strength < 3) {
        strengthProgress.classList.add('weak');
        strengthText.textContent = 'Fraca';
      } else if (strength < 4) {
        strengthProgress.classList.add('medium');
        strengthText.textContent = 'Média';
      } else {
        strengthProgress.classList.add('strong');
        strengthText.textContent = 'Forte';
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

  if (cepInput) {
    cepInput.addEventListener('input', function(e) {
      let value = e.target.value.replace(/\D/g, '');
      if (value.length > 8) value = value.slice(0, 8);
      
      if (value.length > 5) {
        value = value.slice(0, 5) + '-' + value.slice(5);
      }
      
      e.target.value = value;
    });

    cepInput.addEventListener('blur', function() {
      const cep = cepInput.value.replace(/\D/g, '');
      
      if (cep.length === 8) {
        fetch(`https://viacep.com.br/ws/${cep}/json/`)
          .then(response => response.json())
          .then(data => {
            if (!data.erro) {
              document.getElementById('rua').value = data.logradouro || '';
              document.getElementById('bairro').value = data.bairro || '';
              document.getElementById('cidade').value = data.localidade || '';
              document.getElementById('estado').value = data.uf || '';
              
              document.getElementById('numero').focus();
            }
          })
          .catch(error => {
            console.error('Erro ao buscar CEP:', error);
          });
      }
    });
  }

  if (telefoneInput) {
    telefoneInput.addEventListener('input', function(e) {
      let value = e.target.value.replace(/\D/g, '');
      if (value.length > 11) value = value.slice(0, 11);
      
      if (value.length > 10) {
        value = value.replace(/^(\d{2})(\d{5})(\d{4}).*/, '($1) $2-$3');
      } else if (value.length > 6) {
        value = value.replace(/^(\d{2})(\d{4})(\d{0,4}).*/, '($1) $2-$3');
      } else if (value.length > 2) {
        value = value.replace(/^(\d{2})(\d{0,5})/, '($1) $2');
      } else if (value.length > 0) {
        value = value.replace(/^(\d*)/, '($1');
      }
      
      e.target.value = value;
    });
  }

  if (form) {
    form.addEventListener('submit', function(e) {
      e.preventDefault();
      
      const senha = senhaInput.value;
      const confirmarSenha = confirmarSenhaInput.value;
      
      if (senha !== confirmarSenha) {
        alert('As senhas não coincidem!');
        confirmarSenhaInput.focus();
        return;
      }
      
      if (senha.length < 8) {
        alert('A Senha deve ter no mínimo 8 caracteres!');
        senhaInput.focus();
        return;
      }
      
      const termsCheckbox = form.querySelector('input[name="terms"]');
      if (!termsCheckbox.checked) {
        alert('Você precisa aceitar os Termos de Uso e Política de Privacidade!');
        termsCheckbox.focus();
        return;
      }
      
      form.submit();
    });
  }
});