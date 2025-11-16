/**
 * Medicine Page JavaScript
 * File: static/js/medicine.js
 * Author: Dominik Szewczyk
 */

document.addEventListener('DOMContentLoaded', function() {
    console.log('Medicine page loaded');

    const addProfileBtn = document.querySelector('.add-profile-btn');

    // ✅ Add to Profile with AJAX (no page reload)
    if (addProfileBtn && addProfileBtn.tagName === 'BUTTON') {
        setupAddToProfile(addProfileBtn);
    }

    // ✅ Smooth Animations (sections fade in one by one)
    animateMedicineInfo();
});

/**
 * ✅ Add to Profile with AJAX - saves without reloading page
 */
function setupAddToProfile(addProfileBtn) {
    const form = addProfileBtn.closest('form');
    
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const formData = new FormData(this);
        
        // Show loading state
        addProfileBtn.disabled = true;
        const originalText = addProfileBtn.textContent;
        addProfileBtn.textContent = 'Adding...';
        
        try {
            const response = await fetch('/api/profile/add-medicine', {
                method: 'POST',
                body: formData
            });
            
            const data = await response.json();
            
            if (response.ok && data.success) {
                // ✅ Success
                addProfileBtn.textContent = '✓ Added to Profile';
                addProfileBtn.style.backgroundColor = '#28a745';
                
                // Show success notification
                showNotification('Medicine added to your profile!', 'success');
                
                setTimeout(() => {
                    addProfileBtn.disabled = false;
                }, 2000);
            } else {
                // ✅ Error
                addProfileBtn.textContent = originalText;
                addProfileBtn.disabled = false;
                
                // Show error notification
                showNotification(data.error || data.message || 'Failed to add medicine', 'error');
            }
        } catch (error) {
            console.error('Error:', error);
            addProfileBtn.textContent = originalText;
            addProfileBtn.disabled = false;
            
            // Show error notification
            showNotification('Network error. Please try again.', 'error');
        }
    });
}

/**
 * ✅ Success/Error Notifications - popup in corner
 */
function showNotification(message, type = 'info') {
    // Remove existing notification
    const existingNotif = document.querySelector('.notification');
    if (existingNotif) {
        existingNotif.remove();
    }

    // Create notification
    const notification = document.createElement('div');
    notification.className = 'notification';
    notification.textContent = message;
    
    // Colors based on type
    const colors = {
        success: '#28a745',  // 🟢 Green
        error: '#dc3545',    // 🔴 Red
        info: '#17a2b8'      // 🔵 Blue
    };
    
    notification.style.position = 'fixed';
    notification.style.top = '20px';
    notification.style.right = '20px';
    notification.style.backgroundColor = colors[type] || colors.info;
    notification.style.color = 'white';
    notification.style.padding = '15px 20px';
    notification.style.borderRadius = '8px';
    notification.style.boxShadow = '0 4px 12px rgba(0,0,0,0.15)';
    notification.style.zIndex = '1000';
    notification.style.fontSize = '0.95rem';
    notification.style.fontWeight = '500';
    notification.style.animation = 'slideIn 0.3s ease';
    
    document.body.appendChild(notification);
    
    // Add slide in/out animations
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideIn {
            from {
                transform: translateX(400px);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }
        @keyframes slideOut {
            from {
                transform: translateX(0);
                opacity: 1;
            }
            to {
                transform: translateX(400px);
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(style);
    
    // Remove after 3 seconds
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

/**
 * ✅ Smooth Animations - sections fade in one by one
 */
function animateMedicineInfo() {
    const medicineHeader = document.querySelector('.medicine-header');
    const medicineDescription = document.querySelector('.medicine-description');
    const adviceBox = document.querySelector('.advice-box');
    const warningBox = document.querySelector('.warning-box');
    const pubmedLink = document.querySelector('.pubmed-link');
    
    const elements = [medicineHeader, medicineDescription, adviceBox, warningBox, pubmedLink];
    
    elements.forEach((element, index) => {
        if (element) {
            element.style.opacity = '0';
            element.style.transform = 'translateY(20px)';
            element.style.transition = 'all 0.5s ease';
            
            setTimeout(() => {
                element.style.opacity = '1';
                element.style.transform = 'translateY(0)';
            }, 100 + (index * 100)); // Each element appears 100ms after previous
        }
    });
}