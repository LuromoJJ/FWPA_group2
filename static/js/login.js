/**
 * Login Page JavaScript
 * File: static/js/login.js
 * Author: Dominik Szewczyk
 */

document.addEventListener('DOMContentLoaded', function() {
    console.log('Login page loaded');

    const passwordInput = document.getElementById('password');

    // ✅ Password Show/Hide Toggle
    addPasswordToggle(passwordInput);

    // ✅ Form Animations
    animateFormEntry();
});

/**
 * Add password visibility toggle (eye icon)
 */
function addPasswordToggle(passwordInput) {
    const formGroup = passwordInput.closest('.form-group');
    
    const toggleBtn = document.createElement('button');
    toggleBtn.type = 'button';
    toggleBtn.textContent = '👁️';
    toggleBtn.style.position = 'absolute';
    toggleBtn.style.right = '10px';
    toggleBtn.style.top = '50%';
    toggleBtn.style.transform = 'translateY(-50%)';
    toggleBtn.style.border = 'none';
    toggleBtn.style.background = 'none';
    toggleBtn.style.cursor = 'pointer';
    toggleBtn.style.fontSize = '1.2rem';
    
    formGroup.style.position = 'relative';
    
    toggleBtn.addEventListener('click', function() {
        if (passwordInput.type === 'password') {
            passwordInput.type = 'text';
            toggleBtn.textContent = '🙈';
        } else {
            passwordInput.type = 'password';
            toggleBtn.textContent = '👁️';
        }
    });
    
    formGroup.appendChild(toggleBtn);
}

/**
 * Animate form entry - smooth fade in from bottom
 */
function animateFormEntry() {
    const loginCard = document.querySelector('.login-card');
    if (loginCard) {
        loginCard.style.opacity = '0';
        loginCard.style.transform = 'translateY(30px)';
        loginCard.style.transition = 'all 0.5s ease';
        
        setTimeout(() => {
            loginCard.style.opacity = '1';
            loginCard.style.transform = 'translateY(0)';
        }, 100);
    }
}
async function checkEmailAvailability(email) {
    const emailInput = document.getElementById('email');
    const formGroup = emailInput.closest('.form-group');
    
    // Remove previous availability message
    const existingMsg = formGroup.querySelector('.availability-message');
    if (existingMsg) existingMsg.remove();
    
    try {
        const response = await fetch(`/api/auth/check-email?email=${encodeURIComponent(email)}`);
        const data = await response.json();
        
        const msgDiv = document.createElement('div');
        msgDiv.className = 'availability-message';
        msgDiv.style.fontSize = '0.85rem';
        msgDiv.style.marginTop = '5px';

        if (data.available) {
            msgDiv.style.color = '#28a745';
            msgDiv.textContent = '✓ Email is available';
            emailInput.style.borderColor = ''; // reset border
        } else {
            msgDiv.style.color = '#dc3545';
            msgDiv.textContent = '✗ Email already in use';
            emailInput.style.borderColor = '#dc3545';
        }

        formGroup.appendChild(msgDiv);
    } catch (error) {
        console.error('Error checking email:', error);
    }
}