/**
 * Populate AI/ML Section Dynamically
 * Fetches AI/ML articles from data cache and displays them
 */

document.addEventListener('DOMContentLoaded', function() {
    populateAISection();
});

async function populateAISection() {
    try {
        // Fetch the data cache
        const response = await fetch('/data_cache.json');
        if (!response.ok) {
            console.log('Data cache not available yet');
            return;
        }

        const data = await response.json();
        const aiArticles = data.ai_ml_articles || [];

        if (aiArticles.length === 0) {
            console.log('No AI/ML articles available');
            return;
        }

        // Get the AI articles grid container
        const aiGrid = document.getElementById('ai-articles-grid');
        if (!aiGrid) {
            console.log('AI grid container not found');
            return;
        }

        // Clear existing placeholder content
        aiGrid.innerHTML = '';

        // Populate with AI/ML articles
        aiArticles.forEach((article, index) => {
            const articleCard = createAIArticleCard(article, index);
            aiGrid.appendChild(articleCard);
        });

        console.log(`Populated ${aiArticles.length} AI/ML articles`);
    } catch (error) {
        console.error('Error populating AI section:', error);
    }
}

function createAIArticleCard(article, index) {
    const card = document.createElement('article');
    card.className = 'article-card';
    card.style.background = 'white';

    // Create slug for article link
    const slug = article.title
        .toLowerCase()
        .replace(/[^a-z0-9\s-]/g, '')
        .replace(/\s+/g, '-')
        .replace(/^-+|-+$/g, '')
        .substring(0, 50);

    card.innerHTML = `
        <div class="article-image">
            <img alt="${article.title}" src="${article.image}"/>
            <span class="category-badge" style="background: #0097A7;">${article.category}</span>
        </div>
        <div class="article-content">
            <h3 class="article-title">${article.title}</h3>
            <p class="article-excerpt">${article.excerpt}</p>
            <div class="article-footer">
                <div class="author-small">
                    <img alt="${article.author}" src="https://i.pravatar.cc/40?img=${index + 8}"/>
                    <span>${article.author}</span>
                </div>
                <span class="read-time">${article.reading_time} min read</span>
            </div>
        </div>
    `;

    // Make card clickable
    card.style.cursor = 'pointer';
    card.addEventListener('click', function() {
        window.location.href = `/article/${slug}`;
    });

    return card;
}
