function closePopup(popupId) {
            const popup = document.getElementById(popupId);
            if (popup) {
                popup.classList.remove('show');
                document.body.style.overflow = '';
            }
        }

        function showPopup(popupId) {
            const popup = document.getElementById(popupId);
            if (popup) {
                popup.classList.add('show');
                document.body.style.overflow = 'hidden';
            }
        }

        function isUserLoggedIn() {
            return sessionStorage.getItem('user_logged_in') === 'true' || 
                   localStorage.getItem('user_logged_in') === 'true' ||
                   document.cookie.includes('session=') ||
                   document.cookie.includes('token=') ||
                   document.cookie.includes('user_id=');
        }

        document.addEventListener('DOMContentLoaded', function() {
            let selectedSize = null;
            
            const sizeBtns = document.querySelectorAll('.size-btn');
            const tamanhoInput = document.getElementById('tamanho-input');
            const qtyInput = document.getElementById('quantidade-input');
            const qtyMinus = document.getElementById('qty-minus');
            const qtyPlus = document.getElementById('qty-plus');
            const addCartBtn = document.getElementById('add-cart-btn');
            const form = document.getElementById('add-to-cart-form');

            sizeBtns.forEach(btn => {
                btn.addEventListener('click', function(e) {
                    e.preventDefault();
                    e.stopPropagation();
                    
                    sizeBtns.forEach(b => b.classList.remove('selected'));
                    this.classList.add('selected');
                    selectedSize = this.getAttribute('data-size');
                    
                    if (tamanhoInput) {
                        tamanhoInput.value = selectedSize;
                    }
                    
                    console.log('Tamanho selecionado:', selectedSize);
                });
            });

            if (qtyMinus) {
                qtyMinus.addEventListener('click', function(e) {
                    e.preventDefault();
                    e.stopPropagation();
                    
                    if (qtyInput) {
                        let currentValue = parseInt(qtyInput.value) || 1;
                        if (currentValue > 1) {
                            qtyInput.value = currentValue - 1;
                            console.log('Quantidade:', qtyInput.value);
                        }
                    }
                });
            }

            if (qtyPlus) {
                qtyPlus.addEventListener('click', function(e) {
                    e.preventDefault();
                    e.stopPropagation();
                    
                    if (qtyInput) {
                        let currentValue = parseInt(qtyInput.value) || 1;
                        let maxValue = parseInt(qtyInput.getAttribute('max')) || 999;
                        if (currentValue < maxValue) {
                            qtyInput.value = currentValue + 1;
                            console.log('Quantidade:', qtyInput.value);
                        }
                    }
                });
            }

            if (qtyInput) {
                qtyInput.addEventListener('input', function() {
                    let value = parseInt(this.value) || 1;
                    let maxValue = parseInt(this.getAttribute('max')) || 999;
                    
                    if (value < 1) {
                        this.value = 1;
                    } else if (value > maxValue) {
                        this.value = maxValue;
                    }
                });

                qtyInput.addEventListener('change', function() {
                    if (!this.value || parseInt(this.value) < 1) {
                        this.value = 1;
                    }
                });
            }

            if (addCartBtn) {
                addCartBtn.addEventListener('click', function(e) {
                    e.preventDefault();
                    e.stopPropagation();
                    
                    console.log('Botão clicado');
                    console.log('Tamanho selecionado:', selectedSize);
                    console.log('Usuário logado:', isUserLoggedIn());
                    
                    if (!selectedSize || !tamanhoInput.value) {
                        console.log('Mostrando popup de tamanho');
                        showPopup('size-popup');
                        return;
                    }
                    
                    if (!isUserLoggedIn()) {
                        console.log('Mostrando popup de login');
                        showPopup('login-popup');
                        return;
                    }
                    
                    console.log('Enviando formulário');
                    if (form) {
                        form.submit();
                    }
                });
            }

            const sizePopup = document.getElementById('size-popup');
            const loginPopup = document.getElementById('login-popup');

            if (sizePopup) {
                sizePopup.addEventListener('click', function(e) {
                    if (e.target === this) {
                        closePopup('size-popup');
                    }
                });
            }

            if (loginPopup) {
                loginPopup.addEventListener('click', function(e) {
                    if (e.target === this) {
                        closePopup('login-popup');
                    }
                });
            }

            document.addEventListener('keydown', function(e) {
                if (e.key === 'Escape') {
                    if (sizePopup && sizePopup.classList.contains('show')) {
                        closePopup('size-popup');
                    }
                    if (loginPopup && loginPopup.classList.contains('show')) {
                        closePopup('login-popup');
                    }
                }
            });

            console.log('Script carregado - Elementos encontrados:', {
                sizeBtns: sizeBtns.length,
                qtyInput: !!qtyInput,
                qtyMinus: !!qtyMinus,
                qtyPlus: !!qtyPlus,
                addCartBtn: !!addCartBtn,
                form: !!form,
                sizePopup: !!sizePopup,
                loginPopup: !!loginPopup
            });
        });

        window.testLogin = function() {
            sessionStorage.setItem('user_logged_in', 'true');
            console.log('✓ Login simulado - tente adicionar ao carrinho');
        };

        window.testLogout = function() {
            sessionStorage.removeItem('user_logged_in');
            localStorage.removeItem('user_logged_in');
            console.log('✓ Logout simulado - popup deve aparecer');
        }