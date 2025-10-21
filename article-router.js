class ArticleRouter {
    constructor() {
        this.articlesData = null;
        this.currentArticle = null;
        this.init();
    }

    async init() {
        try {
            await this.loadArticlesData();
            const slug = this.getArticleSlugFromURL();
            if (slug) {
                await this.loadArticle(slug);
            } else {
                this.showError();
            }
        } catch (error) {
            console.error('Router initialization error:', error);
            this.showError();
        }
    }

    async loadArticlesData() {
        try {
            const response = await fetch('articles-data.json');
            if (!response.ok) {
                throw new Error('Failed to load articles data');
            }
            const data = await response.json();
            this.articlesData = data.articles;
        } catch (error) {
            console.error('Error loading articles data:', error);
            throw error;
        }
    }

    getArticleSlugFromURL() {
        const hash = window.location.hash;
        const searchParams = new URLSearchParams(window.location.search);
        if (hash) {
            const hashMatch = hash.match(/#\/?(?:article\/)?([a-z0-9-]+)/);
            if (hashMatch) {
                return hashMatch[1];
            }
        }
        return searchParams.get('id') || searchParams.get('article');
    }

    async loadArticle(slug) {
        const article = this.articlesData.find(a => a.slug === slug || a.id === slug);
        if (!article) {
            this.showError();
            return;
        }
        this.currentArticle = article;
        this.displayArticle(article);
        this.loadRelatedArticles(article);
        this.hideLoading();
    }

    displayArticle(article) {
        document.title = `${article.title} - TORQ Tech News`;
        this.updateMetaTags(article);
        document.getElementById('article-category').textContent = article.category;
        document.getElementById('article-date').textContent = this.formatDate(article.date);
        document.getElementById('article-title').textContent = article.title;
        document.getElementById('article-excerpt').textContent = article.excerpt;
        document.getElementById('author-avatar').src = article.author.avatar;
        document.getElementById('author-avatar').alt = article.author.name;
        document.getElementById('author-name').textContent = article.author.name;
        document.getElementById('author-title').textContent = article.author.title;
        document.getElementById('article-read-time').textContent = article.readTime;
        const featuredImage = document.getElementById('article-image');
        featuredImage.src = article.image;
        featuredImage.alt = article.title;
        document.getElementById('article-content').innerHTML = article.content;
        document.getElementById('author-bio-avatar').src = article.author.avatar;
        document.getElementById('author-bio-avatar').alt = article.author.name;
        document.getElementById('author-bio-name').textContent = article.author.name;
        document.getElementById('author-bio-text').textContent = article.author.bio;
        document.getElementById('article-container').style.display = 'block';
    }

    loadRelatedArticles(currentArticle) {
        const relatedArticles = this.articlesData
            .filter(a => a.category === currentArticle.category && a.id !== currentArticle.id)
            .slice(0, 3);
        if (relatedArticles.length < 3) {
            const additionalArticles = this.articlesData
                .filter(a => a.id !== currentArticle.id && !relatedArticles.includes(a))
                .slice(0, 3 - relatedArticles.length);
            relatedArticles.push(...additionalArticles);
        }
        const relatedContainer = document.getElementById('related-articles');
        relatedContainer.innerHTML = relatedArticles.map(article => `
            <a href="article.html?id=${article.slug}" class="related-article-card">
                <img src="${article.image}" alt="${article.title}" class="related-article-image">
                <div class="related-article-content">
                    <span class="related-article-category">${article.category}</span>
                    <h4 class="related-article-title">${article.title}</h4>
                    <div class="related-article-meta">
                        <span>${article.author.name}</span>
                        <span class="separator">•</span>
                        <span>${article.readTime}</span>
                    </div>
                </div>
            </a>
        `).join('');
    }

    formatDate(dateString) {
        const date = new Date(dateString);
        const options = { year: 'numeric', month: 'long', day: 'numeric' };
        return date.toLocaleDateString('en-US', options);
    }

    updateMetaTags(article) {
        this.setMetaTag('description', article.excerpt);
        this.setMetaTag('og:title', article.title, 'property');
        this.setMetaTag('og:description', article.excerpt, 'property');
        this.setMetaTag('og:image', article.image, 'property');
        this.setMetaTag('og:type', 'article', 'property');
        this.setMetaTag('twitter:card', 'summary_large_image');
        this.setMetaTag('twitter:title', article.title);
        this.setMetaTag('twitter:description', article.excerpt);
        this.setMetaTag('twitter:image', article.image);
    }

    setMetaTag(name, content, attribute = 'name') {
        let meta = document.querySelector(`meta[${attribute}="${name}"]`);
        if (!meta) {
            meta = document.createElement('meta');
            meta.setAttribute(attribute, name);
            document.head.appendChild(meta);
        }
        meta.setAttribute('content', content);
    }

    showError() {
        document.getElementById('loading').style.display = 'none';
        document.getElementById('error').style.display = 'flex';
    }

    hideLoading() {
        document.getElementById('loading').style.display = 'none';
    }
}

function shareOnTwitter() {
    const url = window.location.href;
    const text = document.getElementById('article-title').textContent;
    window.open(`https://twitter.com/intent/tweet?url=${encodeURIComponent(url)}&text=${encodeURIComponent(text)}`, '_blank');
}

function shareOnLinkedIn() {
    const url = window.location.href;
    window.open(`https://www.linkedin.com/sharing/share-offsite/?url=${encodeURIComponent(url)}`, '_blank');
}

function copyLink() {
    const url = window.location.href;
    navigator.clipboard.writeText(url).then(() => {
        const btn = event.target.closest('.share-btn');
        const originalText = btn.innerHTML;
        btn.innerHTML = `
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="20 6 9 17 4 12"></polyline>
            </svg>
            Copied!
        `;
        setTimeout(() => {
            btn.innerHTML = originalText;
        }, 2000);
    }).catch(err => {
        console.error('Failed to copy:', err);
        alert('Failed to copy link. Please copy manually.');
    });
}

document.addEventListener('DOMContentLoaded', () => {
    new ArticleRouter();
});
