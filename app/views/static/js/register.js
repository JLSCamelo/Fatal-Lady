// static/js/register.js
document.addEventListener('DOMContentLoaded', function () {
  const form = document.getElementById('register-form');
  if (!form) return;

  const nomeInput = document.getElementById('nome');
  const emailInput = document.getElementById('email');
  const telefoneInput = document.getElementById('telefone');
  const cpfInput = document.getElementById('cpf');
  const dataNascimentoInput = document.getElementById('data_nascimento');
  const generoInput = document.getElementById('genero');

  const cepInput = document.getElementById('cep');
  const ruaInput = document.getElementById('rua');
  const numeroInput = document.getElementById('numero');
  const complementoInput = document.getElementById('complemento');
  const bairroInput = document.getElementById('bairro');
  const cidadeInput = document.getElementById('cidade');
  const estadoInput = document.getElementById('estado');

  const senhaInput = document.getElementById('senha');
  const confirmarSenhaInput = document.getElementById('confirmar-senha');

  const strengthProgress = document.getElementById('strength-progress');
  const strengthText = document.getElementById('strength-text');

  const globalErrorEl = document.getElementById('form-global-error');

  // ================== Helpers de Erro ==================

  function clearFieldError(input) {
    if (!input) return;
    input.classList.remove('input-error');
    const row = input.closest('.input-row');
    if (!row) return;
    const err = row.querySelector('.field-error');
    if (err) err.remove();
  }

  function setFieldError(input, message) {
    if (!input) return;
    input.classList.add('input-error');
    const row = input.closest('.input-row');
    if (!row) return;

    let err = row.querySelector('.field-error');
    if (!err) {
      err = document.createElement('p');
      err.className = 'field-error';
      row.appendChild(err);
    }
    err.textContent = message;
  }

  function clearAllErrors() {
    [
      nomeInput,
      emailInput,
      telefoneInput,
      cpfInput,
      dataNascimentoInput,
      generoInput,
      cepInput,
      ruaInput,
      numeroInput,
      complementoInput,
      bairroInput,
      cidadeInput,
      estadoInput,
      senhaInput,
      confirmarSenhaInput
    ].forEach((input) => clearFieldError(input));
    hideGlobalError();
  }

  function showGlobalError(message) {
    if (!globalErrorEl) return;
    globalErrorEl.textContent = message || '';
    globalErrorEl.hidden = !message;
  }

  function hideGlobalError() {
    if (!globalErrorEl) return;
    globalErrorEl.hidden = true;
    globalErrorEl.textContent = '';
  }

  // Limpar erros enquanto digita
  [
    nomeInput,
    emailInput,
    telefoneInput,
    cpfInput,
    dataNascimentoInput,
    generoInput,
    cepInput,
    ruaInput,
    numeroInput,
    complementoInput,
    bairroInput,
    cidadeInput,
    estadoInput,
    senhaInput,
    confirmarSenhaInput
  ].forEach((input) => {
    if (!input) return;
    input.addEventListener('input', () => {
      clearFieldError(input);
      hideGlobalError();
    });
  });

  // ================== Força da senha ==================

  if (senhaInput && strengthProgress && strengthText) {
    senhaInput.addEventListener('input', function () {
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

  // ================== CEP (máscara + ViaCEP) ==================

  if (cepInput) {
    cepInput.addEventListener('input', function (e) {
      let value = e.target.value.replace(/\D/g, '');
      if (value.length > 8) value = value.slice(0, 8);

      if (value.length > 5) {
        value = value.slice(0, 5) + '-' + value.slice(5);
      }

      e.target.value = value;
    });

    cepInput.addEventListener('blur', function () {
      clearFieldError(cepInput);
      hideGlobalError();

      const cep = cepInput.value.replace(/\D/g, '');
      if (cep.length === 8) {
        fetch(`https://viacep.com.br/ws/${cep}/json/`)
          .then((response) => response.json())
          .then((data) => {
            if (!data.erro) {
              if (ruaInput) ruaInput.value = data.logradouro || '';
              if (bairroInput) bairroInput.value = data.bairro || '';
              if (cidadeInput) cidadeInput.value = data.localidade || '';
              if (estadoInput) estadoInput.value = data.uf || '';
              if (numeroInput) numeroInput.focus();
            }
          })
          .catch((error) => {
            console.error('Erro ao buscar CEP:', error);
          });
      }
    });
  }

  // ================== Telefone (máscara) ==================

  if (telefoneInput) {
    telefoneInput.addEventListener('input', function (e) {
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

  // ================== CPF (máscara) ==================

  if (cpfInput) {
    cpfInput.addEventListener('input', function (e) {
      let value = e.target.value.replace(/\D/g, '');
      if (value.length > 11) value = value.slice(0, 11);

      // mesma máscara usada antes, mas mais segura
      if (value.length <= 3) {
        e.target.value = value;
      } else if (value.length <= 6) {
        e.target.value = value.replace(/(\d{3})(\d{1,3})/, '$1.$2');
      } else if (value.length <= 9) {
        e.target.value = value.replace(
          /(\d{3})(\d{3})(\d{1,3})/,
          '$1.$2.$3'
        );
      } else {
        e.target.value = value.replace(
          /(\d{3})(\d{3})(\d{3})(\d{1,2})/,
          '$1.$2.$3-$4'
        );
      }
    });
  }

  // ================== Validações ==================

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    clearAllErrors();

    let valid = true;

    const emailRegex =
      /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;

    const senha = senhaInput ? senhaInput.value : '';
    const confirmarSenha = confirmarSenhaInput
      ? confirmarSenhaInput.value
      : '';

    const hasNumber = /\d/;
    const hasSpecialChar = /[^a-zA-Z0-9]/;

    // Nome
    if (nomeInput && !nomeInput.value.trim()) {
      setFieldError(nomeInput, 'Informe seu nome completo.');
      valid = false;
    }

    // Email
    if (emailInput) {
      const email = emailInput.value.trim();
      if (!emailRegex.test(email)) {
        setFieldError(
          emailInput,
          'Informe um e-mail válido (ex: seu@exemplo.com).'
        );
        valid = false;
      }
    }

    // Telefone
    if (telefoneInput) {
      const telDigits = telefoneInput.value.replace(/\D/g, '');
      if (telDigits.length < 10) {
        setFieldError(
          telefoneInput,
          'Informe um telefone válido com DDD (mínimo 10 dígitos).'
        );
        valid = false;
      }
    }

    // CPF
    if (cpfInput) {
      const cpfDigits = cpfInput.value.replace(/\D/g, '');
      if (!cpfDigits) {
        setFieldError(cpfInput, 'Informe seu CPF.');
        valid = false;
      } else if (!isValidCpf(cpfDigits)) {
        setFieldError(
          cpfInput,
          'CPF inválido. Verifique os números digitados.'
        );
        valid = false;
      }
    }

    // Data de nascimento
    if (dataNascimentoInput) {
      const value = dataNascimentoInput.value;

      if (!value) {
        setFieldError(
          dataNascimentoInput,
          'Informe sua data de nascimento.'
        );
        valid = false;
      } else {
        const today = new Date();
        const birthDate = new Date(value + 'T00:00:00');

        if (Number.isNaN(birthDate.getTime())) {
          setFieldError(
            dataNascimentoInput,
            'Data de nascimento inválida.'
          );
          valid = false;
        } else {
          if (birthDate > today) {
            setFieldError(
              dataNascimentoInput,
              'A data de nascimento não pode ser futura.'
            );
            valid = false;
          } else {
            const minAge = 16;
            const cutoff = new Date(
              today.getFullYear() - minAge,
              today.getMonth(),
              today.getDate()
            );
            if (birthDate > cutoff) {
              setFieldError(
                dataNascimentoInput,
                `É necessário ter pelo menos ${minAge} anos.`
              );
              valid = false;
            }
          }
        }
      }
    }

    // Gênero
    if (generoInput && !generoInput.value) {
      setFieldError(
        generoInput,
        'Selecione uma opção de gênero.'
      );
      valid = false;
    }

    // CEP
    if (cepInput) {
      const cepDigits = cepInput.value.replace(/\D/g, '');
      if (cepDigits.length !== 8) {
        setFieldError(
          cepInput,
          'Informe um CEP válido (8 dígitos).'
        );
        valid = false;
      }
    }

    // Rua
    if (ruaInput && !ruaInput.value.trim()) {
      setFieldError(ruaInput, 'Informe o nome da rua.');
      valid = false;
    }

    // Número
    if (numeroInput && !numeroInput.value.trim()) {
      setFieldError(numeroInput, 'Informe o número.');
      valid = false;
    }

    // Bairro
    if (bairroInput && !bairroInput.value.trim()) {
      setFieldError(bairroInput, 'Informe o bairro.');
      valid = false;
    }

    // Cidade
    if (cidadeInput && !cidadeInput.value.trim()) {
      setFieldError(cidadeInput, 'Informe a cidade.');
      valid = false;
    }

    // Estado
    if (estadoInput && !estadoInput.value.trim()) {
      setFieldError(estadoInput, 'Selecione o estado.');
      valid = false;
    }

    // Senha
    if (senhaInput) {
      if (!senha) {
        setFieldError(senhaInput, 'Informe uma senha.');
        valid = false;
      } else {
        if (senha.length < 8) {
          setFieldError(
            senhaInput,
            'A senha deve ter no mínimo 8 caracteres.'
          );
          valid = false;
        }
        if (!hasNumber.test(senha)) {
          setFieldError(
            senhaInput,
            'A senha deve conter ao menos um número.'
          );
          valid = false;
        }
        if (!hasSpecialChar.test(senha)) {
          setFieldError(
            senhaInput,
            'A senha deve conter ao menos um caractere especial (ex: !, @, #, $).'
          );
          valid = false;
        }
      }
    }

    // Confirmar senha
    if (confirmarSenhaInput) {
      if (!confirmarSenha) {
        setFieldError(
          confirmarSenhaInput,
          'Confirme a senha informada.'
        );
        valid = false;
      } else if (senha !== confirmarSenha) {
        setFieldError(
          confirmarSenhaInput,
          'As senhas não coincidem.'
        );
        valid = false;
      }
    }

    // Termos
    const termsCheckbox = form.querySelector('input[name="terms"]');
    if (termsCheckbox && !termsCheckbox.checked) {
      showGlobalError(
        'Você precisa aceitar os Termos de Uso e a Política de Privacidade.'
      );
      valid = false;
    }

    if (!valid) {
      if (!globalErrorEl.textContent) {
        showGlobalError('Por favor, corrija os campos destacados.');
      }
      return;
    }

    hideGlobalError();
    form.submit();
  });

  // ================== CPF util ==================

  function isValidCpf(digits) {
    if (!/^\d{11}$/.test(digits)) return false;
    if (/^(\d)\1{10}$/.test(digits)) return false;

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

    return (
      d1 === parseInt(digits.charAt(9), 10) &&
      d2 === parseInt(digits.charAt(10), 10)
    );
  }
});
