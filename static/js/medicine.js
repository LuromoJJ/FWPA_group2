/**
 * Medicine Page JavaScript - Simple Version
 * File: static/js/medicine.js
 */

document.addEventListener('DOMContentLoaded', function() {
    
    // Check if AI is working
    const description = document.querySelector('.medicine-description p');
    if (description && description.textContent.includes('🤖')) {
        showLoadingScreen();
        autoRefreshPage();
    }
    
    // Setup "Add to Profile" button
    setupAddToProfile();
    
    // Animate page sections
    animateSections();
});

// ============================================
// SHOW LOADING SCREEN
// ============================================
function showLoadingScreen() {
    const overlay = document.createElement('div');
    overlay.innerHTML = `
        <div style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; 
                    background: rgba(0,0,0,0.8); z-index: 9999; 
                    display: flex; justify-content: center; align-items: center;">
            <div style="background: white; padding: 40px; border-radius: 16px; text-align: center; max-width: 500px;">
                <div class="spinner"></div>
                <h3 style="margin: 20px 0;">🤖 AI is Researching...</h3>
                <p style="color: #666;">Analyzing medical information</p>
                <div style="width: 100%; height: 8px; background: #e0e0e0; border-radius: 4px; margin: 20px 0; overflow: hidden;">
                    <div class="progress-bar"></div>
                </div>
                <p style="color: #ffc107; font-weight: bold;">Takes 1-3 minutes</p>
                <p id="countdown" style="color: #17a2b8; font-size: 0.9em;">Refreshing in 10 seconds...</p>
            </div>
        </div>
    `;
    
    // Add CSS
    const style = document.createElement('style');
    style.textContent = `
        .spinner {
            width: 50px; height: 50px; margin: 0 auto;
            border: 5px solid #f3f3f3; border-top: 5px solid #90A955;
            border-radius: 50%; animation: spin 1s linear infinite;
        }
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
        .progress-bar {
            width: 0%; height: 100%; background: linear-gradient(90deg, #90A955, #ADC178);
            animation: progress 3s ease-in-out infinite;
        }
        @keyframes progress {
            0% { width: 0%; }
            50% { width: 70%; }
            100% { width: 95%; }
        }
    `;
    document.head.appendChild(style);
    document.body.appendChild(overlay);
}

// ============================================
// AUTO REFRESH PAGE
// ============================================
function autoRefreshPage() {
    let seconds = 10;
    
    const countdown = setInterval(() => {
        seconds--;
        const countdownEl = document.getElementById('countdown');
        if (countdownEl) {
            countdownEl.textContent = `Refreshing in ${seconds} seconds...`;
        }
    }, 1000);
    
    setTimeout(() => {
        clearInterval(countdown);
        location.reload();
    }, 10000);
}

// ============================================
// ADD TO PROFILE BUTTON
// ============================================
function setupAddToProfile() {
    const button = document.querySelector('.add-profile-btn');
    if (!button || button.tagName !== 'BUTTON') return;
    
    const form = button.closest('form');
    
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        button.disabled = true;
        button.textContent = 'Adding...';
        
        const formData = new FormData(this);
        
        try {
            const response = await fetch('/api/profile/add-medicine', {
                method: 'POST',
                body: formData
            });
            
            const data = await response.json();
            
            if (data.success) {
                button.textContent = '✓ Added!';
                button.style.backgroundColor = '#28a745';
                showNotification('Medicine added to profile!', 'success');
            } else {
                button.textContent = '+ Add to My Profile';
                button.disabled = false;
                showNotification(data.error || 'Failed', 'error');
            }
        } catch (error) {
            button.textContent = '+ Add to My Profile';
            button.disabled = false;
            showNotification('Network error', 'error');
        }
    });
}

// ============================================
// SHOW NOTIFICATION
// ============================================
function showNotification(message, type) {
    const colors = {
        success: '#28a745',
        error: '#dc3545',
        info: '#17a2b8'
    };
    
    const notif = document.createElement('div');
    notif.textContent = message;
    notif.style.cssText = `
        position: fixed; top: 20px; right: 20px; z-index: 1000;
        background: ${colors[type]}; color: white; padding: 15px 20px;
        border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    `;
    
    document.body.appendChild(notif);
    
    setTimeout(() => notif.remove(), 3000);
}

// ============================================
// ANIMATE SECTIONS
// ============================================
function animateSections() {
    const sections = [
        document.querySelector('.medicine-header'),
        document.querySelector('.medicine-description'),
        document.querySelector('.advice-box'),
        document.querySelector('.warning-box'),
        document.querySelector('.pubmed-link')
    ];
    
    sections.forEach((section, i) => {
        if (section) {
            section.style.opacity = '0';
            section.style.transform = 'translateY(20px)';
            section.style.transition = 'all 0.5s ease';
            
            setTimeout(() => {
                section.style.opacity = '1';
                section.style.transform = 'translateY(0)';
            }, 100 + (i * 100));
        }
    });
}