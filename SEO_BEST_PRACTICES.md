# SEO Best Practices for TORQ Tech News

## Overview
This document outlines SEO optimization strategies for TORQ Tech News based on Google's SEO Starter Guide and industry best practices.

---

## 1. Meta Descriptions and Title Tags

### Title Tag Best Practices
- **Unique titles for each page** - Every article and page should have a distinct title
- **Descriptive and accurate** - Clearly describe the page content
- **Include primary keywords** naturally
- **Optimal length**: 50-60 characters (to prevent truncation in search results)
- **Format**: `Article Title - TORQ Tech News`

**Example:**
```html
<title>AI Productivity Gains: Team Leaders Write the Rules - TORQ Tech News</title>
```

### Meta Description Best Practices
- **Unique descriptions** for each page
- **Compelling copy** that encourages clicks
- **Include relevant keywords** naturally
- **Optimal length**: 150-160 characters
- **Summarize** the most valuable content on the page

**Example:**
```html
<meta name="description" content="Discover how team leaders can maximize AI productivity gains by establishing clear rules and frameworks. Expert insights from MIT Sloan Management Review.">
```

---

## 2. Content Quality Guidelines

### High-Quality Content Principles
✅ **Original and unique** - Not copied from other sources
✅ **Helpful and reliable** - Provides genuine value to readers
✅ **Well-organized** - Clear headings, short paragraphs, bullet points
✅ **Up-to-date** - Current information with recent dates
✅ **Easy to read** - Clear language, proper grammar
✅ **Mobile-friendly** - Readable on all devices
✅ **Comprehensive** - Thoroughly covers the topic
✅ **Properly attributed** - Credits sources and original publishers

### Content to Avoid
❌ Duplicate content across multiple pages
❌ Keyword stuffing or unnatural keyword use
❌ Thin content with little substance
❌ Distracting ads that interfere with reading
❌ Misleading or clickbait headlines

---

## 3. URL Structure

### Best Practices for URLs
- **Descriptive and meaningful** - Use real words, not IDs
- **Include keywords** relevant to the page
- **Use hyphens** to separate words (not underscores)
- **Keep URLs short** and simple
- **Organize in logical directories** (e.g., `/article/`, `/category/`)

**Good Examples:**
```
https://torqtechnews.com/article/ai-productivity-team-leaders
https://torqtechnews.com/category/artificial-intelligence
https://torqtechnews.com/author/mit-sloan-review
```

**Bad Examples:**
```
https://torqtechnews.com/article?id=12345
https://torqtechnews.com/page_2024_10_16_article
```

---

## 4. Mobile Optimization

### Mobile-First Indexing Requirements
- **Responsive design** - Content adapts to screen size
- **Fast loading** - Optimize images and minimize code
- **Touch-friendly** - Buttons and links easy to tap
- **Readable fonts** - Minimum 16px for body text
- **No horizontal scrolling** required

### Testing
- Use Google Mobile-Friendly Test: https://search.google.com/test/mobile-friendly
- Test on real devices (phones and tablets)
- Check Core Web Vitals in Google Search Console

---

## 5. Image Optimization

### Image SEO Best Practices
- **Descriptive filenames** - `ai-productivity-chart.jpg` not `IMG_12345.jpg`
- **Alt text** - Describe image content for accessibility and SEO
- **Compressed images** - Use WebP or optimized JPEG/PNG
- **Responsive images** - Use `srcset` for different screen sizes
- **Place contextually** - Near relevant text content
- **Include captions** when helpful

**Example:**
```html
<img src="/images/ai-productivity-chart.jpg"
     alt="Chart showing 34% increase in productivity with AI team frameworks"
     loading="lazy">
```

---

## 6. Internal Linking Strategy

### Internal Link Best Practices
- **Descriptive anchor text** - "Read our AI productivity guide" not "click here"
- **Link to related content** - Help users discover relevant articles
- **Logical site structure** - Create topic clusters
- **Use breadcrumbs** for navigation
- **Link from high-traffic pages** to important content

**Example Internal Linking Structure:**
```
Homepage
├── AI & Machine Learning (category)
│   ├── AI Productivity Guide
│   ├── Machine Learning Frameworks
│   └── AI in Enterprise
├── Leadership (category)
│   └── Team Management Best Practices
└── About / Contact
```

---

## 7. Structured Data (Schema Markup)

### Article Schema Implementation
Use JSON-LD structured data for news articles:

```json
{
  "@context": "https://schema.org",
  "@type": "NewsArticle",
  "headline": "AI Productivity Gains: Team Leaders Write the Rules",
  "image": "https://torqtechnews.com/images/article-image.jpg",
  "datePublished": "2025-10-16T00:00:00Z",
  "dateModified": "2025-10-16T12:00:00Z",
  "author": {
    "@type": "Organization",
    "name": "MIT Sloan Review"
  },
  "publisher": {
    "@type": "Organization",
    "name": "TORQ Tech News",
    "logo": {
      "@type": "ImageObject",
      "url": "https://torqtechnews.com/torq-logo.svg"
    }
  },
  "description": "Discover how team leaders can maximize AI productivity..."
}
```

### Other Useful Schema Types
- **BreadcrumbList** - Navigation breadcrumbs
- **WebSite** - Site-wide search box
- **Organization** - Company information
- **Person** - Author profiles

Test structured data: https://search.google.com/test/rich-results

---

## 8. Page Speed Optimization

### Core Web Vitals
- **LCP (Largest Contentful Paint)**: < 2.5 seconds
- **FID (First Input Delay)**: < 100 milliseconds
- **CLS (Cumulative Layout Shift)**: < 0.1

### Optimization Techniques
- Minimize JavaScript and CSS
- Enable browser caching
- Use CDN for static assets
- Lazy load images below the fold
- Compress text files (gzip/brotli)
- Optimize font loading

---

## 9. Sitemap and Robots.txt

### XML Sitemap
Create and submit sitemap to Google Search Console:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://torqtechnews.com/</loc>
    <lastmod>2025-10-16</lastmod>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>https://torqtechnews.com/article/ai-productivity</loc>
    <lastmod>2025-10-16</lastmod>
    <priority>0.8</priority>
  </url>
</urlset>
```

### Robots.txt
```
User-agent: *
Allow: /
Sitemap: https://torqtechnews.com/sitemap.xml

User-agent: *
Disallow: /api/
Disallow: /admin/
```

---

## 10. Content Strategy for News Aggregation

### Legal and Ethical Content Practices
✅ **Proper attribution** - Always credit original sources
✅ **Fair use excerpts** - Limit to 25% of original content or 1-2 paragraphs
✅ **Link to originals** - Include "Read full article at [Source]"
✅ **Unique value** - Add commentary, categorization, or summaries
✅ **Respect robots.txt** - Honor site scraping policies

### Content Display Strategy
1. **For aggregated content:**
   - Display headline + excerpt (300-500 words)
   - Include source logo and attribution
   - Link to full article with clear CTA

2. **For original commentary:**
   - Provide unique insights and analysis
   - Reference source material appropriately
   - Build topical authority with expert perspectives

---

## 11. Technical SEO Checklist

### Essential Technical Elements
- [ ] HTTPS enabled (SSL certificate)
- [ ] Sitemap.xml created and submitted
- [ ] Robots.txt configured properly
- [ ] Canonical tags on all pages
- [ ] 404 pages return proper status codes
- [ ] Redirect chains eliminated
- [ ] Mobile-responsive design implemented
- [ ] Page load speed < 3 seconds
- [ ] No broken links (internal or external)
- [ ] Structured data implemented

### Google Search Console Setup
1. Verify site ownership
2. Submit sitemap
3. Monitor Core Web Vitals
4. Check mobile usability
5. Review indexing status
6. Track search performance

---

## 12. Ongoing SEO Maintenance

### Monthly Tasks
- Review Google Search Console for errors
- Update old content with new information
- Check for broken links
- Monitor page speed metrics
- Analyze top-performing content

### Quarterly Tasks
- Comprehensive site audit
- Update sitemap
- Review and update meta descriptions
- Analyze competitor SEO strategies
- Refresh underperforming content

### Annual Tasks
- Major content refresh for top articles
- Site structure reorganization if needed
- Schema markup updates
- Technical infrastructure review

---

## 13. Measuring SEO Success

### Key Metrics to Track
- **Organic traffic** - Users from Google search
- **Search rankings** - Position for target keywords
- **Click-through rate (CTR)** - Clicks / impressions
- **Bounce rate** - Users leaving after one page
- **Average session duration** - Time on site
- **Pages per session** - Content engagement
- **Core Web Vitals** - Page experience metrics

### Tools
- Google Search Console (free)
- Google Analytics 4 (free)
- Lighthouse (Chrome DevTools)
- PageSpeed Insights
- Ahrefs / SEMrush (paid)

---

## 14. TORQ Tech News Specific Implementation

### Priority SEO Tasks
1. ✅ Implement unique title tags for all articles
2. ✅ Add compelling meta descriptions
3. ✅ Add Article schema markup
4. ✅ Create XML sitemap
5. ✅ Optimize image alt text
6. ✅ Improve internal linking between articles
7. ✅ Implement breadcrumb navigation
8. ✅ Add source attribution for aggregated content

### Target Keywords
Primary: "tech news", "AI news", "technology insights"
Secondary: "Hacker News aggregator", "MIT Sloan research", "business technology"
Long-tail: "latest AI productivity tools", "semiconductor industry news"

---

## Resources

- Google SEO Starter Guide: https://developers.google.com/search/docs/fundamentals/seo-starter-guide
- Google Search Console: https://search.google.com/search-console
- Schema.org Documentation: https://schema.org
- Web.dev (Performance): https://web.dev
- Lighthouse: https://developers.google.com/web/tools/lighthouse

---

**Last Updated:** October 16, 2025
**Version:** 1.0
**Maintained by:** Claude Code for TORQ Tech News
