/**
 * Signup Page JavaScript
 * File: static/js/signup.js
 * Author: Dominik Szewczyk
 */

document.addEventListener('DOMContentLoaded', function() {
    console.log('Signup page loaded');

    const emailInput = document.getElementById('email');
    const passwordInput = document.getElementById('password');
    const confirmPasswordInput = document.getElementById('confirm-password');

    // ✅ Real-time Email Availability Check
    setupEmailAvailabilityCheck(emailInput);

    // ✅ Password Strength Indicator
    setupPasswordStrength(passwordInput);

    // ✅ Password Match Validation
    setupPasswordMatch(passwordInput, confirmPasswordInput);

    // ✅ Password Show/Hide Toggles (for both fields)
    addPasswordToggle(passwordInput);
    addPasswordToggle(confirmPasswordInput);

    // ✅ Form Animations
    animateFormEntry();
});

/**
 * ✅ Real-time Email Availability Check
 */
function setupEmailAvailabilityCheck(emailInput) {
    let emailCheckTimeout;
    
    emailInput.addEventListener('input', function() {
        clearTimeout(emailCheckTimeout);
        
        // Remove previous availability message
        const formGroup = emailInput.closest('.form-group');
        const existingMsg = formGroup.querySelector('.availability-message');
        if (existingMsg) {
            existingMsg.remove();
        }
        
        const email = this.value.trim();
        
        // Only check if email looks valid
        if (email && email.includes('@')) {
            emailCheckTimeout = setTimeout(() => {
                checkEmailAvailability(email);
            }, 500); // Wait 500ms after user stops typing
        }
    });
}


async function checkEmailAvailability(email) {
    const emailInput = document.getElementById('email');
    const formGroup = emailInput.closest('.form-group');

    const oldMsg = formGroup.querySelector('.availability-message');
    if (oldMsg) oldMsg.remove();

    emailInput.style.borderColor = '';

    try {
        const response = await fetch(`/api/auth/check-email?email=${encodeURIComponent(email)}`);
        const data = await response.json();

        console.log('Email check response:', data);

        const msgDiv = document.createElement('div');
        msgDiv.className = 'availability-message';
        msgDiv.style.fontSize = '0.85rem';
        msgDiv.style.marginTop = '5px';

        const isTaken =
            data === true ||
            data?.exists === true ||
            data?.available === false;

        if (!isTaken) {
            msgDiv.style.color = '#28a745';
            msgDiv.textContent = '✓ Email is available';
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
/**
 * ✅ Password Strength Indicator
 */
function setupPasswordStrength(passwordInput) {
    passwordInput.addEventListener('input', function() {
        updatePasswordStrength(this.value);
    });
}

function updatePasswordStrength(password) {
    const passwordInput = document.getElementById('password');
    const formGroup = passwordInput.closest('.form-group');
    
    // Get or create strength indicator
    let strengthDiv = formGroup.querySelector('.password-strength');
    if (!strengthDiv) {
        strengthDiv = document.createElement('div');
        strengthDiv.className = 'password-strength';
        strengthDiv.style.fontSize = '0.85rem';
        strengthDiv.style.marginTop = '5px';
        formGroup.appendChild(strengthDiv);
    }
    
    if (!password) {
        strengthDiv.textContent = '';
        return;
    }
    
    // Calculate strength
    let strength = 0;
    let strengthText = '';
    let strengthColor = '';
    
    if (password.length >= 8) strength++;
    if (password.length >= 12) strength++;
    if (/[a-z]/.test(password) && /[A-Z]/.test(password)) strength++;
    if (/[0-9]/.test(password)) strength++;
    if (/[^a-zA-Z0-9]/.test(password)) strength++;
    
    if (strength <= 2) {
        strengthText = '🔴 Weak password';
        strengthColor = '#dc3545';
    } else if (strength <= 3) {
        strengthText = '🟡 Medium password';
        strengthColor = '#ffc107';
    } else {
        strengthText = '🟢 Strong password';
        strengthColor = '#28a745';
    }
    
    strengthDiv.textContent = strengthText;
    strengthDiv.style.color = strengthColor;
}

/**
 *  Password Match Validation
 */
function setupPasswordMatch(passwordInput, confirmPasswordInput) {
    confirmPasswordInput.addEventListener('input', function() {
        const formGroup = this.closest('.form-group');
        
        // Remove existing match message
        const existingMsg = formGroup.querySelector('.match-message');
        if (existingMsg) {
            existingMsg.remove();
        }
        
        if (this.value && passwordInput.value !== this.value) {
            // Passwords don't match
            const msgDiv = document.createElement('div');
            msgDiv.className = 'match-message';
            msgDiv.style.color = '#dc3545';
            msgDiv.style.fontSize = '0.85rem';
            msgDiv.style.marginTop = '5px';
            msgDiv.textContent = 'Passwords do not match';
            
            formGroup.appendChild(msgDiv);
            this.style.borderColor = '#dc3545';
        } else if (this.value && passwordInput.value === this.value) {
            // Passwords match
            this.style.borderColor = '#28a745';
        } else {
            this.style.borderColor = '';
        }
    });
}

/**
 * ✅ Password Show/Hide Toggle (eye icon)
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
 * ✅ Form Animations - signup card slides up and fades in
 */
function animateFormEntry() {
    const signupCard = document.querySelector('.signup-card');
    if (signupCard) {
        signupCard.style.opacity = '0';
        signupCard.style.transform = 'translateY(30px)';
        signupCard.style.transition = 'all 0.5s ease';
        
        setTimeout(() => {
            signupCard.style.opacity = '1';
            signupCard.style.transform = 'translateY(0)';
        }, 100);
    }
}