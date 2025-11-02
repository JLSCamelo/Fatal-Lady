document.addEventListener('DOMContentLoaded', function() {
    const quantityInputs = document.querySelectorAll('.quantity-input');
    const removeButtons = document.querySelectorAll('.btn-remove');
    const quantityForms = document.querySelectorAll('.quantity-control');
    
    quantityInputs.forEach(input => {
        input.addEventListener('input', function() {
            if (this.value < 1) {
                this.value = 1;
            }
            
            const maxValue = 999;
            if (this.value > maxValue) {
                this.value = maxValue;
            }
        });

        input.addEventListener('blur', function() {
            if (!this.value || this.value === '' || this.value < 1) {
                this.value = 1;
            }
        });
    });

    removeButtons.forEach(button => {
        const form = button.closest('form');
        
        form.addEventListener('submit', function(e) {
            const cartItem = this.closest('.cart-item');
            if (cartItem) {
                cartItem.classList.add('removing');
            }
            
            button.textContent = 'Removendo...';
            button.disabled = true;
        });
    });

    quantityForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitButton = this.querySelector('button[type="submit"]');
            const input = this.querySelector('.quantity-input');
            
            if (input && (!input.value || input.value < 1)) {
                e.preventDefault();
                input.value = 1;
                return false;
            }
            
            if (submitButton) {
                submitButton.textContent = 'Salvando...';
                submitButton.disabled = true;
            }
        });
    });

    function updateCartTotal() {
        const cartItems = document.querySelectorAll('.cart-item:not(.removing)');
        let subtotal = 0;

        cartItems.forEach(item => {
            const priceElement = item.querySelector('.item-price');
            const quantityInput = item.querySelector('.quantity-input');
            
            if (priceElement && quantityInput) {
                const priceText = priceElement.dataset.price || priceElement.textContent.replace('R$', '').trim();
                const price = parseFloat(priceText.replace(',', '.'));
                const quantity = parseInt(quantityInput.value) || 1;
                
                if (!isNaN(price) && !isNaN(quantity)) {
                    subtotal += price * quantity;
                }
            }
        });

        const subtotalElement = document.getElementById('subtotal');
        const totalElement = document.getElementById('total');
        const shippingElement = document.getElementById('shipping');

        if (subtotalElement) {
            subtotalElement.textContent = `R$ ${subtotal.toFixed(2).replace('.', ',')}`;
        }

        if (totalElement) {
            totalElement.textContent = `R$ ${subtotal.toFixed(2).replace('.', ',')}`;
        }

        if (shippingElement) {
            if (subtotal >= 299) {
                shippingElement.textContent = 'Grátis';
                shippingElement.style.color = '#22c55e';
            } else {
                shippingElement.textContent = 'A calcular';
                shippingElement.style.color = '#666';
            }
        }
    }

    quantityInputs.forEach(input => {
        input.addEventListener('change', updateCartTotal);
    });

    if (quantityInputs.length > 0) {
        updateCartTotal();
    }

    const checkoutButton = document.querySelector('.btn-checkout');
    if (checkoutButton) {
        const checkoutForm = checkoutButton.closest('form');
        if (checkoutForm) {
            checkoutForm.addEventListener('submit', function() {
                checkoutButton.textContent = 'Processando...';
                checkoutButton.disabled = true;
            });
        }
    }
});