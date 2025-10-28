document.addEventListener('DOMContentLoaded', function() {
    
    const isUserLoggedIn = () => {
        return sessionStorage.getItem('user_logged_in') === 'true' || 
               localStorage.getItem('user_logged_in') === 'true' ||
               document.cookie.includes('session=') ||
               document.cookie.includes('token=');
    };

    const showLoginModal = () => {
        const modal = document.getElementById('login-modal');
        if (modal) {
            modal.classList.add('show');
            document.body.style.overflow = 'hidden';
        }
    };

    const hideLoginModal = () => {
        const modal = document.getElementById('login-modal');
        if (modal) {
            modal.classList.remove('show');
            document.body.style.overflow = '';
        }
    };

    const sizeBtns = document.querySelectorAll('.size-btn');
    const tamanhoInput = document.getElementById('tamanho-input');
    const sizeError = document.getElementById('size-error');

    sizeBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            sizeBtns.forEach(b => b.classList.remove('selected'));
            btn.classList.add('selected');
            if (tamanhoInput) {
                tamanhoInput.value = btn.dataset.size;
            }
            
            const optionGroup = btn.closest('.option-group');
            if (optionGroup) {
                optionGroup.classList.remove('error');
            }
            if (sizeError) {
                sizeError.classList.remove('show');
            }
            
            console.log('Tamanho selecionado:', btn.dataset.size);
        });
    });

    const qtyInput = document.getElementById('quantidade-input');
    const qtyMinus = document.getElementById('qty-minus');
    const qtyPlus = document.getElementById('qty-plus');
    const qtyError = document.getElementById('qty-error');

    const updateQuantity = (change) => {
        if (!qtyInput) return;
        
        const current = parseInt(qtyInput.value) || 1;
        const max = parseInt(qtyInput.max) || 999;
        const newValue = Math.max(1, Math.min(max, current + change));
        qtyInput.value = newValue;
        
        const optionGroup = qtyInput.closest('.option-group');
        if (optionGroup) {
            optionGroup.classList.remove('error');
        }
        if (qtyError) {
            qtyError.classList.remove('show');
        }
        
        console.log('Quantidade atualizada:', newValue);
    };

    if (qtyMinus) {
        qtyMinus.addEventListener('click', (e) => {
            e.preventDefault();
            updateQuantity(-1);
        });
    }

    if (qtyPlus) {
        qtyPlus.addEventListener('click', (e) => {
            e.preventDefault();
            updateQuantity(1);
        });
    }

    if (qtyInput) {
        qtyInput.addEventListener('input', () => {
            const max = parseInt(qtyInput.max) || 999;
            let value = parseInt(qtyInput.value) || 1;
            
            if (value < 1) value = 1;
            if (value > max) value = max;
            
            qtyInput.value = value;
        });

        qtyInput.addEventListener('change', () => {
            const max = parseInt(qtyInput.max) || 999;
            let value = parseInt(qtyInput.value) || 1;
            
            if (value < 1) value = 1;
            if (value > max) value = max;
            
            qtyInput.value = value;
        });
    }

    const form = document.getElementById('add-to-cart-form');

    const validateForm = () => {
        let isValid = true;
        
        if (!tamanhoInput || !tamanhoInput.value) {
            const sizeGroup = document.querySelector('#size-selector');
            if (sizeGroup) {
                const optionGroup = sizeGroup.closest('.option-group');
                if (optionGroup) {
                    optionGroup.classList.add('error');
                }
            }
            if (sizeError) {
                sizeError.classList.add('show');
            }
            isValid = false;
            console.log('Erro: Tamanho não selecionado');
        }
        
        if (qtyInput) {
            const qty = parseInt(qtyInput.value);
            const max = parseInt(qtyInput.max);
            
            if (!qty || qty < 1 || qty > max) {
                const qtyGroup = qtyInput.closest('.option-group');
                if (qtyGroup) {
                    qtyGroup.classList.add('error');
                }
                if (qtyError) {
                    qtyError.classList.add('show');
                    qtyError.textContent = qty > max 
                        ? `Estoque máximo: ${max} unidades` 
                        : 'Quantidade inválida';
                }
                isValid = false;
                console.log('Erro: Quantidade inválida');
            }
        }
        
        return isValid;
    };

    if (form) {
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            
            console.log('Tentando adicionar ao carrinho...');
            console.log('Usuário logado?', isUserLoggedIn());
            
            if (!isUserLoggedIn()) {
                console.log('Usuário não está logado - abrindo modal');
                showLoginModal();
                return;
            }
            
            console.log('Validando formulário...');
            if (!validateForm()) {
                const firstError = document.querySelector('.option-group.error');
                if (firstError) {
                    firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
                }
                return;
            }
            
            console.log('Formulário válido - enviando...');
            form.submit();
        });
    }

    const modal = document.getElementById('login-modal');
    const modalClose = document.querySelector('.modal-close');

    if (modalClose) {
        modalClose.addEventListener('click', (e) => {
            e.preventDefault();
            hideLoginModal();
        });
    }

    if (modal) {
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                hideLoginModal();
            }
        });
    }

    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && modal && modal.classList.contains('show')) {
            hideLoginModal();
        }
    });

    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
    });

    const mainImg = document.getElementById('main-product-img');

    if (mainImg) {
        mainImg.addEventListener('mouseenter', () => {
            mainImg.style.transform = 'scale(1.05)';
            mainImg.style.transition = 'transform 0.3s ease';
        });

        mainImg.addEventListener('mouseleave', () => {
            mainImg.style.transform = 'scale(1)';
        });
    }

    console.log('Product page JS carregado com sucesso!');
    console.log('Elementos encontrados:', {
        form: !!form,
        sizeBtns: sizeBtns.length,
        qtyInput: !!qtyInput,
        modal: !!modal
    });
});
