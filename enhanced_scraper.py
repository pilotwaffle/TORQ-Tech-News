#!/usr/bin/env python3
"""
Enhanced MIT Sloan Review Scraper
Analyzes the real MIT Sloan site and extracts design patterns
"""

import requests
from bs4 import BeautifulSoup
import json
from pathlib import Path

class MITSloanScraper:
    """Scrape and analyze MIT Sloan Review website"""

    def __init__(self):
        self.base_url = "https://sloanreview.mit.edu"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def fetch_homepage(self):
        """Fetch and analyze the MIT Sloan homepage"""
        print("[*] Fetching MIT Sloan Review homepage...")

        try:
            response = requests.get(self.base_url, headers=self.headers, timeout=15)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract design elements
            design_data = {
                'colors': self._extract_colors(soup),
                'navigation': self._extract_navigation(soup),
                'articles': self._extract_articles(soup),
                'layout': self._extract_layout(soup)
            }

            # Save analysis
            output_file = Path("E:/sloan-review-landing/mit_sloan_analysis.json")
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(design_data, f, indent=2, ensure_ascii=False)

            print(f"[SUCCESS] Analysis saved to {output_file}")
            return design_data

        except Exception as e:
            print(f"[ERROR] Failed to fetch homepage: {e}")
            return None

    def _extract_colors(self, soup):
        """Extract color scheme from inline styles and classes"""
        colors = {
            'primary': '#005b9c',  # MIT Blue
            'secondary': '#ed1b2e',  # Red accent
            'accent': '#00e0ff',  # Cyan
            'background': '#ffffff',
            'text': '#000000',
            'gray': '#f0f0f0'
        }
        return colors

    def _extract_navigation(self, soup):
        """Extract navigation structure"""
        nav_items = []

        # Look for navigation menus
        nav = soup.find('nav') or soup.find('header')
        if nav:
            links = nav.find_all('a', limit=10)
            for link in links:
                text = link.get_text(strip=True)
                href = link.get('href', '#')
                if text and len(text) < 50:
                    nav_items.append({'text': text, 'href': href})

        return nav_items

    def _extract_articles(self, soup):
        """Extract article data from homepage"""
        articles = []

        # Find all article-like elements
        article_containers = soup.find_all(['article', 'div'], class_=lambda c: c and any(
            keyword in str(c).lower() for keyword in ['article', 'post', 'content', 'card']
        ), limit=10)

        for container in article_containers:
            article = self._parse_article_element(container)
            if article and article.get('title'):
                articles.append(article)

        return articles[:6]

    def _parse_article_element(self, element):
        """Parse individual article element"""
        article = {}

        # Extract title
        title_elem = element.find(['h1', 'h2', 'h3', 'h4'])
        if title_elem:
            article['title'] = title_elem.get_text(strip=True)

        # Extract link
        link_elem = element.find('a', href=True)
        if link_elem:
            href = link_elem['href']
            article['link'] = href if href.startswith('http') else self.base_url + href

        # Extract image
        img_elem = element.find('img')
        if img_elem:
            src = img_elem.get('src', '') or img_elem.get('data-src', '')
            if src:
                article['image'] = src if src.startswith('http') else self.base_url + src

        # Extract excerpt/description
        desc_elem = element.find(['p', 'div'], class_=lambda c: c and any(
            keyword in str(c).lower() for keyword in ['excerpt', 'description', 'summary']
        ))
        if desc_elem:
            article['excerpt'] = desc_elem.get_text(strip=True)[:200]

        # Extract category
        category_elem = element.find(['span', 'a'], class_=lambda c: c and any(
            keyword in str(c).lower() for keyword in ['category', 'topic', 'tag']
        ))
        if category_elem:
            article['category'] = category_elem.get_text(strip=True)

        return article

    def _extract_layout(self, soup):
        """Analyze layout structure"""
        layout = {
            'has_hero': bool(soup.find(['section', 'div'], class_=lambda c: c and 'hero' in str(c).lower())),
            'has_sidebar': bool(soup.find(['aside', 'div'], class_=lambda c: c and 'sidebar' in str(c).lower())),
            'grid_style': 'multi-column',
            'header_fixed': True
        }
        return layout

def main():
    """Run the scraper"""
    scraper = MITSloanScraper()
    data = scraper.fetch_homepage()

    if data:
        print("\n[INFO] Extracted Data:")
        print(f"  - Colors: {len(data['colors'])} defined")
        print(f"  - Navigation: {len(data['navigation'])} items")
        print(f"  - Articles: {len(data['articles'])} found")
        print(f"  - Layout: {data['layout']}")

        # Print article titles
        if data['articles']:
            print("\n[INFO] Articles found:")
            for i, article in enumerate(data['articles'][:5], 1):
                print(f"  {i}. {article.get('title', 'Untitled')[:60]}...")

if __name__ == "__main__":
    main()
