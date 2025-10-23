/**
 * Populate Main Articles Section Dynamically
 * Fetches articles from data cache and displays them with proper slugs
 */

document.addEventListener('DOMContentLoaded', function() {
    populateMainArticles();
});

async function populateMainArticles() {
    try {
        // Fetch the data cache
        const response = await fetch('/data_cache.json');
        if (!response.ok) {
            console.log('Data cache not available yet - using static HTML');
            return;
        }

        const data = await response.json();
        const articles = data.articles || [];

        if (articles.length === 0) {
            console.log('No articles available');
            return;
        }

        // Get the main articles grid container
        const articlesGrid = document.getElementById('articles-grid');
        if (!articlesGrid) {
            console.log('Main articles grid container not found');
            return;
        }

        // Clear existing articles
        articlesGrid.innerHTML = '';

        // Populate with articles (show up to 6)
        articles.slice(0, 6).forEach((article, index) => {
            const articleCard = createArticleCard(article, index);
            articlesGrid.appendChild(articleCard);
        });

        console.log(`Populated ${Math.min(articles.length, 6)} main articles`);
    } catch (error) {
        console.error('Error populating main articles:', error);
    }
}

function createArticleCard(article, index) {
    const card = document.createElement('article');
    card.className = 'article-card';

    // Use slug from data if available, otherwise generate from title
    let slug = article.slug;
    if (!slug || slug === 'NO SLUG') {
        slug = article.title
            .toLowerCase()
            .replace(/[^a-z0-9\s-]/g, '')
            .replace(/\s+/g, '-')
            .replace(/^-+|-+$/g, '')
            .substring(0, 50);
    }

    // Add slug as data attribute for click handler
    card.dataset.slug = slug;

    // Determine category badge color
    const categoryColors = {
        'Data & AI': '#0097A7',
        'Leadership': '#7E57C2',
        'Sustainability': '#66BB6A',
        'Strategy': '#FF7043',
        'Innovation': '#42A5F5'
    };
    const categoryColor = categoryColors[article.category] || '#616161';

    card.innerHTML = `
        <div class="article-image">
            <img alt="${escapeHtml(article.title)}" src="${article.image}"/>
            <span class="category-badge" style="background: ${categoryColor};">${escapeHtml(article.category)}</span>
        </div>
        <div class="article-content">
            <h3 class="article-title">${escapeHtml(article.title)}</h3>
            <p class="article-excerpt">${escapeHtml(article.excerpt || article.author)}</p>
            <div class="article-footer">
                <div class="author-small">
                    <img alt="${escapeHtml(article.author)}" src="https://i.pravatar.cc/40?img=${index + 1}"/>
                    <span>${escapeHtml(article.author)}</span>
                </div>
                <span class="read-time">${article.reading_time || 7} min read</span>
            </div>
        </div>
    `;

    // Make card clickable
    card.style.cursor = 'pointer';

    return card;
}

function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}
