/**
 * MIT Sloan Management Review - JavaScript
 * Interactive functionality for the landing page
 */

// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize all features
    initMobileMenu();
    initNewsletterForm();
    initSmoothScrolling();
    initScrollAnimations();
});

/**
 * Mobile Menu Toggle
 */
function initMobileMenu() {
    const navToggle = document.getElementById('navToggle');
    const navMenu = document.getElementById('navMenu');

    if (!navToggle || !navMenu) return;

    navToggle.addEventListener('click', function() {
        navToggle.classList.toggle('active');
        navMenu.classList.toggle('active');
    });

    // Close menu when clicking on a link
    const navLinks = navMenu.querySelectorAll('a');
    navLinks.forEach(link => {
        link.addEventListener('click', function() {
            navToggle.classList.remove('active');
            navMenu.classList.remove('active');
        });
    });

    // Close menu when clicking outside
    document.addEventListener('click', function(event) {
        const isClickInsideNav = navToggle.contains(event.target) || navMenu.contains(event.target);
        if (!isClickInsideNav && navMenu.classList.contains('active')) {
            navToggle.classList.remove('active');
            navMenu.classList.remove('active');
        }
    });
}

/**
 * Newsletter Form Handling
 */
function initNewsletterForm() {
    const form = document.getElementById('newsletterForm');

    if (!form) return;

    form.addEventListener('submit', function(event) {
        event.preventDefault();

        const emailInput = form.querySelector('input[type="email"]');
        const submitButton = form.querySelector('button[type="submit"]');

        if (!emailInput || !submitButton) return;

        const email = emailInput.value.trim();

        // Basic email validation
        if (!isValidEmail(email)) {
            showMessage('Please enter a valid email address', 'error');
            return;
        }

        // Disable button and show loading state
        submitButton.disabled = true;
        const originalText = submitButton.textContent;
        submitButton.textContent = 'Subscribing...';

        // Simulate API call (replace with actual API endpoint)
        setTimeout(function() {
            // Success
            showMessage('Thank you for subscribing! Check your inbox for confirmation.', 'success');
            emailInput.value = '';

            // Reset button
            submitButton.disabled = false;
            submitButton.textContent = originalText;

            // Track subscription (analytics)
            trackEvent('Newsletter', 'Subscribe', email);
        }, 1500);
    });
}

/**
 * Email Validation
 */
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

/**
 * Show Message (Success/Error)
 */
function showMessage(message, type = 'success') {
    // Remove existing messages
    const existingMessages = document.querySelectorAll('.success-message, .error-message');
    existingMessages.forEach(msg => msg.remove());

    // Create message element
    const messageEl = document.createElement('div');
    messageEl.className = type === 'success' ? 'success-message' : 'error-message';
    messageEl.textContent = message;

    // Add to page
    document.body.appendChild(messageEl);

    // Remove after 5 seconds
    setTimeout(function() {
        messageEl.style.opacity = '0';
        setTimeout(function() {
            messageEl.remove();
        }, 300);
    }, 5000);
}

/**
 * Smooth Scrolling for Anchor Links
 */
function initSmoothScrolling() {
    const links = document.querySelectorAll('a[href^="#"]');

    links.forEach(link => {
        link.addEventListener('click', function(event) {
            const href = this.getAttribute('href');

            // Skip if href is just "#"
            if (href === '#') return;

            event.preventDefault();

            const targetId = href.substring(1);
            const targetElement = document.getElementById(targetId);

            if (targetElement) {
                const headerHeight = document.querySelector('.header').offsetHeight;
                const targetPosition = targetElement.offsetTop - headerHeight - 20;

                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
}

/**
 * Scroll Animations
 */
function initScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -100px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Observe article cards
    const articleCards = document.querySelectorAll('.article-card');
    articleCards.forEach(card => observer.observe(card));

    // Observe topic cards
    const topicCards = document.querySelectorAll('.topic-card');
    topicCards.forEach(card => observer.observe(card));
}

/**
 * Analytics Event Tracking
 * Replace with your actual analytics implementation (Google Analytics, etc.)
 */
function trackEvent(category, action, label) {
    if (typeof gtag !== 'undefined') {
        gtag('event', action, {
            'event_category': category,
            'event_label': label
        });
    }

    console.log('Event tracked:', category, action, label);
}

/**
 * Card Click Tracking
 */
document.addEventListener('click', function(event) {
    // Track article card clicks
    const articleCard = event.target.closest('.article-card');
    if (articleCard) {
        const title = articleCard.querySelector('.article-title')?.textContent;
        trackEvent('Article', 'Click', title);
    }

    // Track topic card clicks
    const topicCard = event.target.closest('.topic-card');
    if (topicCard) {
        const topic = topicCard.querySelector('h3')?.textContent;
        trackEvent('Topic', 'Click', topic);
    }
});

/**
 * Utility: Debounce function
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * Handle window resize
 */
const handleResize = debounce(function() {
    // Close mobile menu on resize to desktop
    const navToggle = document.getElementById('navToggle');
    const navMenu = document.getElementById('navMenu');

    if (window.innerWidth >= 768 && navMenu && navMenu.classList.contains('active')) {
        navToggle.classList.remove('active');
        navMenu.classList.remove('active');
    }
}, 250);

window.addEventListener('resize', handleResize);

/**
 * Add loading class to page
 */
window.addEventListener('load', function() {
    document.body.classList.add('loaded');
});

console.log('MIT Sloan Management Review - Landing Page Loaded');
