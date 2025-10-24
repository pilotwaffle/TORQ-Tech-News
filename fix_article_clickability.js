/**
 * QUICK FIX: Make article cards clickable using event delegation
 * This works even when articles are loaded dynamically
 *
 * USAGE: Replace the content of make_articles_clickable.js with this code
 */

// Use event delegation on the document body - works for all dynamically added elements
document.body.addEventListener('click', function(e) {
    // Find the closest article card
    const card = e.target.closest('.article-card');

    // If we clicked inside an article card
    if (card) {
        // Don't navigate if clicking on an actual link
        if (e.target.closest('a')) {
            return;
        }

        // Get the slug from data attribute
        const slug = card.dataset.slug;

        // Fallback: If no slug in data attribute, generate from title
        if (!slug || slug === 'NO SLUG') {
            const titleElement = card.querySelector('.article-title');
            if (titleElement) {
                const title = titleElement.textContent.trim();
                const generatedSlug = title
                    .toLowerCase()
                    .replace(/[^a-z0-9\s-]/g, '')
                    .replace(/\s+/g, '-')
                    .replace(/^-+|-+$/g, '')
                    .substring(0, 50);

                console.log('Using generated slug:', generatedSlug);
                window.location.href = `/article/${generatedSlug}`;
            }
        } else {
            // Use the slug from data attribute
            console.log('Navigating to:', `/article/${slug}`);
            window.location.href = `/article/${slug}`;
        }
    }
});

console.log('✅ Article click handler using event delegation installed');
