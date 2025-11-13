/**
 * Make articles clickable and link to full content pages
 * Updated to use data-slug attributes from dynamically loaded articles
 */

document.addEventListener('DOMContentLoaded', function() {
    // Make all article cards clickable
    const articleCards = document.querySelectorAll('.article-card');

    articleCards.forEach(card => {
        card.style.cursor = 'pointer';

        card.addEventListener('click', function(e) {
            // Don't navigate if clicking on a link
            if (e.target.tagName === 'A') return;

            // Try to get slug from data attribute first (preferred)
            let slug = card.dataset.slug;
            
            // Fallback: generate slug from title if no data-slug attribute
            if (!slug) {
                const titleElement = card.querySelector('.article-title');
                if (titleElement) {
                    const title = titleElement.textContent.trim();
                    slug = title
                        .toLowerCase()
                        .replace(/[^a-z0-9\s-]/g, '')
                        .replace(/\s+/g, '-')
                        .replace(/^-+|-+$/g, '')  // Remove leading/trailing dashes
                        .substring(0, 50);
                }
            }

            if (slug) {
                // Navigate to article page
                window.location.href = `/article/${slug}`;
            }
        });
    });

    // Make hero/featured article clickable
    const heroButton = document.querySelector('.hero .btn-large');
    if (heroButton) {
        heroButton.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Try to get slug from hero section data attribute
            const heroSection = document.querySelector('.hero');
            let slug = heroSection?.dataset.slug;
            
            // Fallback: generate from title
            if (!slug) {
                const titleElement = document.querySelector('.hero-title');
                if (titleElement) {
                    const title = titleElement.textContent.trim();
                    slug = title
                        .toLowerCase()
                        .replace(/[^a-z0-9\s-]/g, '')
                        .replace(/\s+/g, '-')
                        .replace(/^-+|-+$/g, '')  // Remove leading/trailing dashes
                        .substring(0, 50);
                }
            }

            if (slug) {
                window.location.href = `/article/${slug}`;
            }
        });
    }
});
