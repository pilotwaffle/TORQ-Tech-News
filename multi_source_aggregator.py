#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TORQ Tech News - Multi-Source News Aggregator
Fetches tech news from multiple sources: MIT Sloan, TechCrunch, MIT Tech Review, Hacker News
"""

import sys
import os

# Force UTF-8 encoding for Windows compatibility
if sys.platform.startswith('win'):
    os.environ['PYTHONIOENCODING'] = 'utf-8'

import os
import json
import time
import re
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
import requests
from bs4 import BeautifulSoup
import random
from newspaper import Article
import hashlib

class MultiSourceAggregator:
    """
    Intelligent aggregator that fetches from multiple tech news sources
    """

    def __init__(self, landing_page_dir: str = None):
        if landing_page_dir is None:
            landing_page_dir = os.path.dirname(os.path.abspath(__file__))
        self.landing_page_dir = Path(landing_page_dir)
        self.data_cache = self.landing_page_dir / "data_cache.json"

        # News sources
        self.sources = {
            "mit_sloan": "https://sloanreview.mit.edu",
            "techcrunch": "https://techcrunch.com",
            "mit_tech_review": "https://www.technologyreview.com",
            "hackernews": "https://news.ycombinator.com"
        }

        # Categories
        self.categories = {
            "AI & Machine Learning": {"color": "#0097A7", "icon": "🧠"},
            "Startups & Funding": {"color": "#E91E63", "icon": "🚀"},
            "Enterprise Tech": {"color": "#607D8B", "icon": "💼"},
            "Innovation": {"color": "#2196F3", "icon": "💡"},
            "Leadership": {"color": "#9C27B0", "icon": "👥"},
            "Technology": {"color": "#4CAF50", "icon": "🤖"}
        }

    def fetch_techcrunch_articles(self, limit: int = 3) -> List[Dict]:
        """Fetch latest articles from TechCrunch"""
        print("[*] Fetching from TechCrunch...")
        articles = []

        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            response = requests.get("https://techcrunch.com/category/artificial-intelligence/",
                                   headers=headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')
            article_elements = soup.find_all('article', class_='post-block', limit=limit)

            for article_elem in article_elements:
                try:
                    # Get title
                    title_elem = article_elem.find(['h2', 'h3'])
                    if not title_elem:
                        continue
                    title = title_elem.get_text(strip=True)

                    # Get link
                    link_elem = article_elem.find('a', href=True)
                    link = link_elem['href'] if link_elem else "#"

                    # Get excerpt
                    excerpt_elem = article_elem.find('div', class_='post-block__content')
                    excerpt = excerpt_elem.get_text(strip=True)[:200] if excerpt_elem else title

                    # Get image
                    img_elem = article_elem.find('img')
                    image = img_elem.get('src', '') if img_elem else self._get_fallback_image()

                    # Get author
                    author_elem = article_elem.find('span', class_='river-byline__authors')
                    author = author_elem.get_text(strip=True) if author_elem else "TechCrunch"

                    articles.append({
                        'title': title[:100],
                        'excerpt': excerpt,
                        'image': image,
                        'category': "AI & Machine Learning",
                        'author': author,
                        'date': datetime.now().strftime("%B %d, %Y"),
                        'reading_time': random.randint(4, 8),
                        'link': link,
                        'source': 'TechCrunch'
                    })
                    print(f"  [OK] TechCrunch: {title[:50]}...")
                except Exception as e:
                    continue

        except Exception as e:
            print(f"[WARN] TechCrunch error: {e}")
            articles = self._generate_techcrunch_fallback(limit)

        return articles[:limit]

    def fetch_mit_tech_review_articles(self, limit: int = 2) -> List[Dict]:
        """Fetch latest articles from MIT Technology Review"""
        print("[*] Fetching from MIT Technology Review...")
        articles = []

        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            response = requests.get("https://www.technologyreview.com/topic/artificial-intelligence/",
                                   headers=headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')
            article_elements = soup.find_all('article', limit=limit)

            for article_elem in article_elements:
                try:
                    # Get title
                    title_elem = article_elem.find(['h2', 'h3', 'a'])
                    if not title_elem:
                        continue
                    title = title_elem.get_text(strip=True)

                    # Get link
                    link_elem = article_elem.find('a', href=True)
                    link = link_elem['href'] if link_elem else "#"
                    if link.startswith('/'):
                        link = "https://www.technologyreview.com" + link

                    # Get excerpt
                    excerpt_elem = article_elem.find('p')
                    excerpt = excerpt_elem.get_text(strip=True)[:200] if excerpt_elem else title

                    # Get image
                    img_elem = article_elem.find('img')
                    image = img_elem.get('src', '') if img_elem else self._get_fallback_image()

                    articles.append({
                        'title': title[:100],
                        'excerpt': excerpt,
                        'image': image,
                        'category': "Innovation",
                        'author': "MIT Technology Review",
                        'date': datetime.now().strftime("%B %d, %Y"),
                        'reading_time': random.randint(8, 12),
                        'link': link,
                        'source': 'MIT Tech Review'
                    })
                    print(f"  [OK] MIT Tech Review: {title[:50]}...")
                except Exception as e:
                    continue

        except Exception as e:
            print(f"[WARN] MIT Tech Review error: {e}")
            articles = self._generate_mit_tech_fallback(limit)

        return articles[:limit]

    def fetch_hackernews_articles(self, limit: int = 2) -> List[Dict]:
        """Fetch top articles from Hacker News using their API"""
        print("[*] Fetching from Hacker News...")
        articles = []

        try:
            # Get top story IDs
            response = requests.get("https://hacker-news.firebaseio.com/v0/topstories.json", timeout=10)
            response.raise_for_status()
            story_ids = response.json()[:limit * 3]  # Get more to filter

            for story_id in story_ids[:limit]:
                try:
                    # Get story details
                    story_response = requests.get(
                        f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json",
                        timeout=5
                    )
                    story = story_response.json()

                    if story and story.get('type') == 'story':
                        title = story.get('title', '')
                        url = story.get('url', f"https://news.ycombinator.com/item?id={story_id}")
                        author = story.get('by', 'HN User')

                        articles.append({
                            'title': title[:100],
                            'excerpt': f"Popular on Hacker News with {story.get('score', 0)} points",
                            'image': self._get_fallback_image(),
                            'category': "Technology",
                            'author': author,
                            'date': datetime.now().strftime("%B %d, %Y"),
                            'reading_time': random.randint(5, 10),
                            'link': url,
                            'slug': self._extract_slug(url, title),
                            'source': 'Hacker News'
                        })
                        print(f"  [OK] Hacker News: {title[:50]}...")

                        if len(articles) >= limit:
                            break
                except Exception as e:
                    continue

        except Exception as e:
            print(f"[WARN] Hacker News error: {e}")
            articles = self._generate_hackernews_fallback(limit)

        return articles[:limit]

    def fetch_mit_sloan_articles(self, limit: int = 1) -> List[Dict]:
        """Fetch articles from MIT Sloan Review"""
        print("[*] Fetching from MIT Sloan Review...")
        articles = []

        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            response = requests.get("https://sloanreview.mit.edu/topic/data-ai-machine-learning/",
                                   headers=headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')
            article_elements = soup.find_all('article', limit=limit)

            for article_elem in article_elements:
                try:
                    title_elem = article_elem.find(['h2', 'h3', 'h4'])
                    if not title_elem:
                        continue

                    title = title_elem.get_text(strip=True)
                    link_elem = article_elem.find('a', href=True)
                    link = link_elem['href'] if link_elem else "#"

                    if link.startswith('/'):
                        link = "https://sloanreview.mit.edu" + link

                    articles.append({
                        'title': title[:100],
                        'excerpt': "Business strategy insights from MIT Sloan School of Management",
                        'image': self._get_fallback_image(),
                        'category': "Leadership",
                        'author': "MIT Sloan Review",
                        'date': datetime.now().strftime("%B %d, %Y"),
                        'reading_time': random.randint(7, 12),
                        'link': link,
                        'slug': self._extract_slug(link, title),
                        'source': 'MIT Sloan'
                    })
                    print(f"  [OK] MIT Sloan: {title[:50]}...")
                except Exception as e:
                    continue

        except Exception as e:
            print(f"[WARN] MIT Sloan error: {e}")

        return articles[:limit]

    def _get_fallback_image(self) -> str:
        """Get a random fallback image"""
        unsplash_ids = [
            'photo-1677442136019-21780ecad995',  # AI
            'photo-1451187580459-43490279c0fa',  # Tech
            'photo-1460925895917-afdab827c52f',  # Data
            'photo-1552664730-d307ca884978',  # Innovation
        ]
        selected = random.choice(unsplash_ids)
        return f"https://images.unsplash.com/{selected}?w=800&h=600&fit=crop"


    def _extract_slug(self, url: str, title: str = "") -> str:
        """Extract slug from URL or generate from title"""
        import re

        # Try to extract from MIT Sloan URL
        if "sloanreview.mit.edu/article/" in url:
            match = re.search(r'/article/([^/]+)/?', url)
            if match:
                return match.group(1)

        # Try to extract from other URL patterns
        if "hackernews" in url or "ycombinator" in url:
            # For HN, use the ID
            match = re.search(r'id=(\d+)', url)
            if match:
                return f"hn-{match.group(1)}"

        # Fallback: generate from title
        if title:
            slug = title.lower()
            slug = re.sub(r'[^a-z0-9\s-]', '', slug)
            slug = re.sub(r'\s+', '-', slug)
            slug = re.sub(r'^-+|-+$', '', slug)
            return slug[:50]

        return "article"



    def _extract_slug(self, url: str, title: str = "") -> str:
        """Extract slug from URL or generate from title"""
        import re

        # Try to extract from MIT Sloan URL
        if "sloanreview.mit.edu/article/" in url:
            match = re.search(r'/article/([^/]+)/?', url)
            if match:
                return match.group(1)

        # Try to extract from other URL patterns
        if "hackernews" in url or "ycombinator" in url:
            # For HN, use the ID
            match = re.search(r'id=(\d+)', url)
            if match:
                return f"hn-{match.group(1)}"

        # Fallback: generate from title
        if title:
            slug = title.lower()
            slug = re.sub(r'[^a-z0-9\s-]', '', slug)
            slug = re.sub(r'\s+', '-', slug)
            slug = re.sub(r'^-+|-+$', '', slug)
            return slug[:50]

        return "article"



    def _extract_slug(self, url: str, title: str = "") -> str:
        """Extract slug from URL or generate from title"""
        import re

        # Try to extract from MIT Sloan URL
        if "sloanreview.mit.edu/article/" in url:
            match = re.search(r'/article/([^/]+)/?', url)
            if match:
                return match.group(1)

        # Try to extract from other URL patterns
        if "hackernews" in url or "ycombinator" in url:
            # For HN, use the ID
            match = re.search(r'id=(\d+)', url)
            if match:
                return f"hn-{match.group(1)}"

        # Fallback: generate from title
        if title:
            slug = title.lower()
            slug = re.sub(r'[^a-z0-9\s-]', '', slug)
            slug = re.sub(r'\s+', '-', slug)
            slug = re.sub(r'^-+|-+$', '', slug)
            return slug[:50]

        return "article"


    def extract_article_content(self, url: str) -> Dict[str, str]:
        """
        Extract full article content from URL using newspaper3k

        Args:
            url: Article URL to extract

        Returns:
            Dict with extracted content (title, text, top_image, authors, publish_date)
        """
        try:
            article = Article(url)
            article.download()
            article.parse()

            # Extract natural language features (keywords, summary)
            try:
                article.nlp()
            except:
                pass  # NLP is optional

            return {
                'title': article.title,
                'text': article.text,
                'top_image': article.top_image,
                'authors': article.authors,
                'publish_date': str(article.publish_date) if article.publish_date else None,
                'summary': article.summary if hasattr(article, 'summary') else '',
                'keywords': article.keywords if hasattr(article, 'keywords') else [],
                'url': url,
                'extracted': True
            }
        except Exception as e:
            print(f"  [WARN] Could not extract content from {url}: {e}")
            return {
                'title': '',
                'text': '',
                'top_image': '',
                'authors': [],
                'publish_date': None,
                'summary': '',
                'keywords': [],
                'url': url,
                'extracted': False,
                'error': str(e)
            }

    def _generate_techcrunch_fallback(self, count: int) -> List[Dict]:
        """Generate TechCrunch fallback articles"""
        titles = [
            "AI Startup Raises $50M to Transform Enterprise Analytics",
            "Google Announces Major AI Model Breakthrough",
            "New Study Shows AI Impact on Productivity"
        ]
        return [{
            'title': titles[i % len(titles)],
            'excerpt': "Latest tech news from Silicon Valley's most influential startups and companies.",
            'image': self._get_fallback_image(),
            'category': "Startups & Funding",
            'author': "TechCrunch",
            'date': datetime.now().strftime("%B %d, %Y"),
            'reading_time': random.randint(4, 7),
            'link': "https://techcrunch.com",
            'source': 'TechCrunch'
        } for i in range(count)]

    def _generate_mit_tech_fallback(self, count: int) -> List[Dict]:
        """Generate MIT Tech Review fallback articles"""
        titles = [
            "The Future of Quantum Computing in Enterprise",
            "Breakthrough in Battery Technology Could Transform EVs"
        ]
        return [{
            'title': titles[i % len(titles)],
            'excerpt': "Deep-dive technology analysis from MIT's leading tech publication.",
            'image': self._get_fallback_image(),
            'category': "Innovation",
            'author': "MIT Technology Review",
            'date': datetime.now().strftime("%B %d, %Y"),
            'reading_time': random.randint(10, 15),
            'link': "https://www.technologyreview.com",
            'source': 'MIT Tech Review'
        } for i in range(count)]

    def _generate_hackernews_fallback(self, count: int) -> List[Dict]:
        """Generate Hacker News fallback articles"""
        titles = [
            "Show HN: New Open Source ML Framework",
            "Ask HN: Best Practices for Scaling Startups"
        ]
        return [{
            'title': titles[i % len(titles)],
            'excerpt': "Trending tech discussions from the developer community.",
            'image': self._get_fallback_image(),
            'category': "Technology",
            'author': "HN Community",
            'date': datetime.now().strftime("%B %d, %Y"),
            'reading_time': random.randint(3, 8),
            'link': "https://news.ycombinator.com",
            'source': 'Hacker News'
        } for i in range(count)]

    def fetch_all_articles(self, extract_content: bool = True) -> Dict:
        """
        Fetch articles from all sources

        Args:
            extract_content: If True, extract full article content using newspaper3k
        """
        print("="*60)
        print("[AGGREGATOR] TORQ Tech News - Multi-Source Aggregator")
        print("="*60)
        print()

        all_articles = []

        # Fetch from each source with delays to be respectful
        techcrunch = self.fetch_techcrunch_articles(3)
        time.sleep(2)  # Rate limiting
        all_articles.extend(techcrunch)

        mit_tech = self.fetch_mit_tech_review_articles(2)
        time.sleep(2)
        all_articles.extend(mit_tech)

        hackernews = self.fetch_hackernews_articles(2)
        time.sleep(1)
        all_articles.extend(hackernews)

        mit_sloan = self.fetch_mit_sloan_articles(6)
        all_articles.extend(mit_sloan)

        # Extract full article content if requested
        if extract_content:
            print()
            print("[*] Extracting full article content...")
            for article in all_articles:
                if article.get('link') and article['link'] not in ['#', '']:
                    print(f"  [*] Extracting: {article['title'][:50]}...")
                    extracted = self.extract_article_content(article['link'])

                    if extracted['extracted']:
                        # Add extracted content to article
                        article['full_text'] = extracted['text']
                        article['summary'] = extracted['summary'] or article.get('excerpt', '')
                        article['keywords'] = extracted['keywords']

                        # Update image if better quality available
                        if extracted['top_image']:
                            article['image'] = extracted['top_image']

                        # Update authors if available
                        if extracted['authors']:
                            article['author'] = ', '.join(extracted['authors'][:2])  # First 2 authors

                        print(f"    [OK] Extracted {len(extracted['text'])} characters")
                    else:
                        # Keep article with just excerpt
                        article['full_text'] = ''
                        article['summary'] = article.get('excerpt', '')
                        article['keywords'] = []
                        print(f"    [SKIP] Using excerpt only")

                    time.sleep(1)  # Rate limiting between extractions

        # Shuffle for diversity
        random.shuffle(all_articles)

        # Take top 6 for main grid
        articles = all_articles[:6]

        # Featured article (best from the bunch)
        featured = all_articles[0] if all_articles else self._get_default_featured()
        featured['author_title'] = "Tech Analyst"

        # AI/ML specific articles
        ai_articles = [a for a in all_articles if "AI" in a['category'] or "Machine" in a['title']][:3]
        if len(ai_articles) < 3:
            ai_articles.extend(techcrunch[:3 - len(ai_articles)])

        cache_data = {
            'timestamp': datetime.now().isoformat(),
            'featured': featured,
            'articles': articles,
            'ai_ml_articles': ai_articles,
            'sources_used': list(set([a.get('source', 'Unknown') for a in all_articles]))
        }

        self.save_cache(cache_data)

        print()
        print("="*60)
        print("[SUCCESS] Multi-source aggregation complete!")
        print(f"[INFO] Total articles: {len(all_articles)}")
        print(f"[INFO] Articles with full content: {sum(1 for a in all_articles if a.get('full_text'))}")
        print(f"[INFO] Sources: {', '.join(cache_data['sources_used'])}")
        print("="*60)

        return cache_data

    def _get_default_featured(self) -> Dict:
        """Get default featured article"""
        return {
            'title': "The Future of AI in Enterprise Technology",
            'excerpt': "How artificial intelligence is transforming business operations and strategy across industries.",
            'image': self._get_fallback_image(),
            'category': "AI & Machine Learning",
            'author': "TORQ Tech News",
            'author_title': "Editorial Team",
            'date': datetime.now().strftime("%B %d, %Y"),
            'reading_time': 10,
            'link': "#"
        }

    def save_cache(self, data: Dict):
        """Save fetched data to cache"""
        with open(self.data_cache, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"[INFO] Data cached to {self.data_cache}")


def main():
    """Entry point"""
    aggregator = MultiSourceAggregator()
    aggregator.fetch_all_articles()


if __name__ == "__main__":
    main()
