/**
 * Homepage JavaScript
 * File: static/js/homepage.js
 * Author: Dominik Szewczyk
 */

document.addEventListener('DOMContentLoaded', function() {
    console.log('Homepage loaded');

    // ✅ Smooth Animations
    animatePageLoad();
});

/**
 * Animate page load - smooth fade in
 */
function animatePageLoad() {
    const hero = document.querySelector('.hero');
    if (hero) {
        hero.style.opacity = '0';
        hero.style.transform = 'translateY(20px)';
        hero.style.transition = 'all 0.6s ease';
        
        setTimeout(() => {
            hero.style.opacity = '1';
            hero.style.transform = 'translateY(0)';
        }, 100);
    }
}