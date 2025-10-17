# Web Scraping Best Practices

## Key Principles for Ethical and Effective Web Scraping

### 1. Rate Limiting and Delays
- **Add delays** between requests (1-3 seconds minimum)
- Use `time.sleep(random.uniform(1, 3))` for randomized delays
- Avoid overwhelming the target server
- MIT Sloan Review: 2-5 second delays recommended

### 2. User-Agent Headers
- **Always set a proper User-Agent** header
- Identify yourself as a bot if appropriate
- Current implementation: `Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36`
- Alternative: Custom user agent with contact info

### 3. Respect robots.txt
- Check `/robots.txt` before scraping
- MIT Sloan Review robots.txt: https://sloanreview.mit.edu/robots.txt
- Follow crawl-delay directives
- Respect disallowed paths

### 4. Error Handling
- **Implement comprehensive try-except blocks**
- Handle network errors gracefully
- Use fallback data when scraping fails
- Log errors for debugging
- Don't crash on single article failure

### 5. Data Cleaning and Validation
- **Validate extracted data** before storing
- Check for empty/null values
- Trim whitespace
- Validate URL formats
- Ensure required fields are present

### 6. Handling Anti-Scraping Measures
- Rotate User-Agents if necessary
- Handle rate limiting (429 errors)
- Implement exponential backoff
- Use proxies only if ethically justified
- Respect site's terms of service

### 7. Caching Strategy
- **Cache scraped data** to reduce requests
- Use timestamps to track freshness
- Implement cache expiration (e.g., 5 hours)
- Store in JSON/database for reuse

### 8. Ethical Considerations
- Don't overload servers
- Respect intellectual property
- Provide attribution for content
- Consider API alternatives
- Follow academic/research guidelines

## Implementation Checklist for TORQ Tech News

- [x] User-Agent headers set
- [x] Error handling with try-except
- [x] Fallback data for failed scrapes
- [x] Data caching (data_cache.json)
- [ ] Rate limiting delays between requests
- [ ] robots.txt compliance check
- [ ] Exponential backoff on errors
- [ ] Request timeout handling
- [x] Multiple topic sources for diversity

## Recommended Improvements

### Add Rate Limiting
```python
import time
import random

time.sleep(random.uniform(2, 5))  # 2-5 second delay
```

### Check robots.txt
```python
from urllib.robotparser import RobotFileParser

rp = RobotFileParser()
rp.set_url("https://sloanreview.mit.edu/robots.txt")
rp.read()
can_fetch = rp.can_fetch("*", url)
```

### Exponential Backoff
```python
for attempt in range(3):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        break
    except requests.exceptions.RequestException:
        if attempt < 2:
            time.sleep(2 ** attempt)  # 1s, 2s, 4s
```

## Resources

- ZenRows Best Practices: https://www.zenrows.com/blog/web-scraping-best-practices
- Python Requests Documentation: https://docs.python-requests.org/
- BeautifulSoup Documentation: https://www.crummy.com/software/BeautifulSoup/
- robots.txt Specification: https://www.robotstxt.org/

## Legal and Ethical Notes

**Always ensure your scraping activities comply with:**
- Website terms of service
- Copyright laws
- Data privacy regulations (GDPR, CCPA, etc.)
- Computer Fraud and Abuse Act (CFAA) in the US
- Academic or professional ethics guidelines

**MIT Sloan Review:**
- Educational/research use: Generally acceptable with attribution
- Commercial use: May require permission
- Attribution: Always link back to original articles
- Current implementation: Links to original MIT Sloan articles
