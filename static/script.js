/**
  script.js
 1. Flash messages auto-dismiss
 2. Delete confirmation
 3. Category badge colors
 4. Number formatting
 */

document.addEventListener('DOMContentLoaded', () => {

    
    // 1. FLASH MESSAGES
    document.querySelectorAll('.flash').forEach((el, i) => {
        setTimeout(() => {
            el.style.transition = 'opacity 0.4s, transform 0.4s';
            el.style.opacity = '0';
            el.style.transform = 'translateY(-8px)';
            setTimeout(() => el.remove(), 400);
        }, 4000 + (i * 200));
    });


    
    // 2. DELETE CONFIRMATION
    document.querySelectorAll('form[data-confirm]').forEach(form => {
        form.addEventListener('submit', (e) => {
            const msg = form.dataset.confirm || 'Are you sure?';
            if (!confirm(msg)) {
                e.preventDefault();
            }
        });
    });


    
    // 3. AUTO-DETECT CATEGORY COLOR
    const categoryColors = {
        'food': 'cat-food',
        'bills': 'cat-bills',
        'travel': 'cat-travel',
        'shopping': 'cat-shopping',
        'health': 'cat-health',
        'other': 'cat-other'
    };

    document.querySelectorAll('.expense-item').forEach(item => {
        const catEl = item.querySelector('.expense-category');
        const badge = item.querySelector('.expense-badge');
        if (!catEl || !badge) return;

        const cat = catEl.textContent.trim().toLowerCase();
        const cls = categoryColors[cat] || 'cat-other';
        badge.classList.add(cls);
    });


    
    // 4. FORM VALIDATION — Password confirm
    const signupForm = document.querySelector('form[action*="signup"]');
    if (signupForm) {
        const pass = signupForm.querySelector('#password');
        const confirm = signupForm.querySelector('#confirm_password');

        confirm.addEventListener('input', () => {
            if (confirm.value && pass.value !== confirm.value) {
                confirm.setCustomValidity('Passwords do not match');
            } else {
                confirm.setCustomValidity('');
            }
        });
    }


    
    // 5. SUBTLE PARALLAX
    document.querySelectorAll('.stat-card').forEach(card => {
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = (e.clientX - rect.left) / rect.width - 0.5;
            const y = (e.clientY - rect.top) / rect.height - 0.5;
            card.style.transform = `translateY(-2px) rotateX(${-y * 3}deg) rotateY(${x * 3}deg)`;
        });

        card.addEventListener('mouseleave', () => {
            card.style.transform = '';
        });
    });


    console.log('Expense Tracker — ready');
});