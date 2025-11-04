document.addEventListener('DOMContentLoaded', function() {
  const form = document.getElementById('register-form');
  const emailInput = document.getElementById('email');
  const senhaInput = document.getElementById('senha');
  const confirmarSenhaInput = document.getElementById('confirmar-senha');
  const cepInput = document.getElementById('cep');
  const telefoneInput = document.getElementById('telefone'); // Já estava sendo capturado
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
      e.preventDefault(); // Impede o envio padrão do formulário
      
      const email = emailInput.value;
      const telefone = telefoneInput.value; // Captura o valor do telefone
      const senha = senhaInput.value;
      const confirmarSenha = confirmarSenhaInput.value;
      
      // Expressões regulares para validação
      const emailRegex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
      const hasNumber = /\d/;
      const hasSpecialChar = /[^a-zA-Z0-9]/;

      // --- VALIDAÇÕES ---

      // 1. Validação de Email
      if (!emailRegex.test(email)) {
        alert('Por favor, insira um email válido (ex: seu@exemplo.com).');
        emailInput.focus();
        return;
      }
      
      // 2. Validação de Telefone (NOVO)
      const telefoneLimpo = telefone.replace(/\D/g, ''); // Remove máscara
      if (telefoneLimpo.length < 10) { // Telefones no Brasil têm 10 (fixo) ou 11 (celular) dígitos com DDD
        alert('Por favor, insira um telefone válido com DDD (mínimo 10 dígitos).');
        telefoneInput.focus();
        return;
      }

      // --- VALIDAÇÕES DE SENHA ---
      
      // 3. Validação de Comprimento Mínimo
      if (senha.length < 8) {
        alert('A Senha deve ter no mínimo 8 caracteres!');
        senhaInput.focus();
        return;
      }
      
      // 4. Validação de Número
      if (!hasNumber.test(senha)) {
        alert('A senha deve conter ao menos um número.');
        senhaInput.focus();
        return;
      }
  
      // 5. Validação de Caracter Especial
      if (!hasSpecialChar.test(senha)) {
        alert('A senha deve conter ao menos um caracter especial (ex: !, @, #, $).');
        senhaInput.focus();
        return;
      }

      // 6. Validação de Confirmação de Senha
      if (senha !== confirmarSenha) {
        alert('As senhas não coincidem!');
        confirmarSenhaInput.focus();
        return;
      }
      
      // --- VALIDAÇÃO DOS TERMOS ---

      // 7.
      const termsCheckbox = form.querySelector('input[name="terms"]');
      if (!termsCheckbox.checked) {
        alert('Você precisa aceitar os Termos de Uso e Política de Privacidade!');
        termsCheckbox.focus();
        return;
      }
      
      // Se todas as validações passarem, envia o formulário
      form.submit();
    });
  }
});