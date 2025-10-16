/**
 * Make articles clickable and link to full content pages
 */

document.addEventListener('DOMContentLoaded', function() {
    // Make all article cards clickable
    const articleCards = document.querySelectorAll('.article-card');

    articleCards.forEach(card => {
        card.style.cursor = 'pointer';

        card.addEventListener('click', function(e) {
            // Don't navigate if clicking on a link
            if (e.target.tagName === 'A') return;

            // Get article title and create slug
            const titleElement = card.querySelector('.article-title');
            if (titleElement) {
                const title = titleElement.textContent.trim();
                const slug = title
                    .toLowerCase()
                    .replace(/[^a-z0-9\s-]/g, '')
                    .replace(/\s+/g, '-')
                    .replace(/^-+|-+$/g, '')  // Remove leading/trailing dashes
                    .substring(0, 50);

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
            const titleElement = document.querySelector('.hero-title');
            if (titleElement) {
                const title = titleElement.textContent.trim();
                const slug = title
                    .toLowerCase()
                    .replace(/[^a-z0-9\s-]/g, '')
                    .replace(/\s+/g, '-')
                    .replace(/^-+|-+$/g, '')  // Remove leading/trailing dashes
                    .substring(0, 50);

                window.location.href = `/article/${slug}`;
            }
        });
    }
});
