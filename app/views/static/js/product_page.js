const isUserLoggedIn = () => {
    return sessionStorage.getItem('user_logged_in') === 'true' || 
           document.cookie.includes('session=');
};

const showLoginModal = () => {
    const modal = document.getElementById('login-modal');
    modal.classList.add('show');
    document.body.style.overflow = 'hidden';
};

const hideLoginModal = () => {
    const modal = document.getElementById('login-modal');
    modal.classList.remove('show');
    document.body.style.overflow = '';
};

const sizeBtns = document.querySelectorAll('.size-btn');
const tamanhoInput = document.getElementById('tamanho-input');
const sizeError = document.getElementById('size-error');

sizeBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        sizeBtns.forEach(b => b.classList.remove('selected'));
        btn.classList.add('selected');
        tamanhoInput.value = btn.dataset.size;
        
        const optionGroup = btn.closest('.option-group');
        optionGroup.classList.remove('error');
        sizeError.classList.remove('show');
    });
});

const qtyInput = document.getElementById('quantidade-input');
const qtyMinus = document.getElementById('qty-minus');
const qtyPlus = document.getElementById('qty-plus');
const qtyError = document.getElementById('qty-error');

const updateQuantity = (change) => {
    const current = parseInt(qtyInput.value) || 1;
    const max = parseInt(qtyInput.max) || 999;
    const newValue = Math.max(1, Math.min(max, current + change));
    qtyInput.value = newValue;
    
    const optionGroup = qtyInput.closest('.option-group');
    optionGroup.classList.remove('error');
    qtyError.classList.remove('show');
};

qtyMinus.addEventListener('click', () => updateQuantity(-1));
qtyPlus.addEventListener('click', () => updateQuantity(1));

qtyInput.addEventListener('input', () => {
    const max = parseInt(qtyInput.max) || 999;
    let value = parseInt(qtyInput.value) || 1;
    
    if (value < 1) value = 1;
    if (value > max) value = max;
    
    qtyInput.value = value;
});

const form = document.getElementById('add-to-cart-form');

const validateForm = () => {
    let isValid = true;
    
    if (!tamanhoInput.value) {
        const sizeGroup = document.querySelector('#size-selector').closest('.option-group');
        sizeGroup.classList.add('error');
        sizeError.classList.add('show');
        isValid = false;
    }
    
    const qty = parseInt(qtyInput.value);
    const max = parseInt(qtyInput.max);
    
    if (!qty || qty < 1 || qty > max) {
        const qtyGroup = qtyInput.closest('.option-group');
        qtyGroup.classList.add('error');
        qtyError.classList.add('show');
        qtyError.textContent = qty > max 
            ? `Estoque máximo: ${max} unidades` 
            : 'Quantidade inválida';
        isValid = false;
    }
    
    return isValid;
};

form.addEventListener('submit', (e) => {
    e.preventDefault();
    
    if (!isUserLoggedIn()) {
        showLoginModal();
        return;
    }
    
    if (!validateForm()) {
        const firstError = document.querySelector('.option-group.error');
        if (firstError) {
            firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
        return;
    }
    
    form.submit();
});

const modal = document.getElementById('login-modal');
const modalClose = document.querySelector('.modal-close');

modalClose?.addEventListener('click', hideLoginModal);

modal?.addEventListener('click', (e) => {
    if (e.target === modal) {
        hideLoginModal();
    }
});

document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && modal?.classList.contains('show')) {
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

mainImg?.addEventListener('mouseenter', () => {
    mainImg.style.transform = 'scale(1.05)';
    mainImg.style.transition = 'transform 0.3s ease';
});

mainImg?.addEventListener('mouseleave', () => {
    mainImg.style.transform = 'scale(1)';
});

console.log('Product page loaded successfully');