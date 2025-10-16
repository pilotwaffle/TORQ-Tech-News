# MIT Sloan Management Review - Automated Landing Page

A beautiful, responsive landing page inspired by MIT Sloan Management Review with **intelligent automation** to populate content.

## 🎯 Features

✅ **Professional Design** - MIT-inspired red color scheme (#A31F34)
✅ **Fully Responsive** - Mobile, tablet, and desktop layouts
✅ **Automated Content** - AI agent populates articles automatically
✅ **6 Article Cards** - Dynamic content with images and metadata
✅ **Newsletter Form** - With validation and success feedback
✅ **Smooth Animations** - Hover effects and scroll animations
✅ **Mobile Menu** - Hamburger menu for small screens
✅ **Data Caching** - Fast subsequent loads

---

## 📁 Project Files

```
E:\sloan-review-landing\
├── index.html              - Main landing page
├── styles.css              - Professional CSS styling (1000+ lines)
├── script.js               - Interactive JavaScript
├── automation_agent.py     - Intelligent content agent
├── data_cache.json         - Cached article data
├── run_automation.bat      - Easy automation runner
└── README.md              - This file
```

---

## 🚀 Quick Start

### 1. View the Landing Page

**Option A: If server is already running**
```
http://localhost:8080
```

**Option B: Start the server**
```bash
cd E:\sloan-review-landing
python -m http.server 8080
```

Or use the full path:
```bash
"E:\Python\Python311\python.exe" -m http.server 8080
```

Then open: **http://localhost:8080**

### 2. Update Content (Run Automation)

**Option A: Use the batch file (Easy!)**
```
Double-click: run_automation.bat
```

**Option B: Command line**
```bash
cd E:\sloan-review-landing
"E:\Python\Python311\python.exe" automation_agent.py
```

---

## 🤖 How the Automation Works

The `automation_agent.py` script:

1. **Attempts to fetch** real articles from MIT Sloan Review
2. **Parses content** - Titles, excerpts, authors, dates, images
3. **Falls back gracefully** - Uses intelligent placeholders if needed
4. **Updates HTML** - Modifies index.html with new content
5. **Caches data** - Saves to data_cache.json for quick access

### What Gets Updated

- ✅ Featured article (hero section)
- ✅ 6 article cards with:
  - Unique titles
  - Category badges (Technology, Leadership, etc.)
  - Author names and avatars
  - Reading times (7-15 min)
  - Dynamic images from Unsplash
  - Publication dates

### Automation Features

- **Intelligent scraping** - Parses MIT Sloan Review website
- **BeautifulSoup parsing** - Extracts structured data
- **Fallback system** - Works even if source is unavailable
- **Data caching** - JSON storage for fast reuse
- **Error handling** - Graceful degradation

---

## 📊 Content Agent Details

### Agent Class: `ContentAgent`

**Main Methods:**
- `fetch_featured_article()` - Gets hero content
- `fetch_articles(limit=6)` - Gets latest articles
- `_parse_article(element)` - Extracts metadata
- `update_html_page(featured, articles)` - Updates HTML
- `save_cache(data)` - Caches to JSON
- `run()` - Main execution flow

### Data Structure

**data_cache.json:**
```json
{
  "timestamp": "2025-10-16T12:39:05",
  "featured": {
    "title": "...",
    "excerpt": "...",
    "author": "...",
    "category": "..."
  },
  "articles": [
    { "title": "...", "author": "...", ... }
  ]
}
```

---

## 🎨 Design Features

### Color Scheme
- **Primary**: #A31F34 (MIT Red)
- **Secondary**: #8A8B8C (MIT Gray)
- **Accent**: #C8102E

### Typography
- **Font**: Inter (Google Fonts)
- **Weights**: 300, 400, 500, 600, 700, 800

### Layout
- **Container**: Max-width 1200px
- **Grid**: CSS Grid for articles (1/2/3 columns responsive)
- **Spacing**: Consistent spacing scale

### Responsive Breakpoints
- **Mobile**: < 640px
- **Tablet**: 640px - 1024px
- **Desktop**: > 1024px

---

## 🔧 Technical Stack

**Frontend:**
- HTML5
- CSS3 (Grid, Flexbox, Custom Properties)
- Vanilla JavaScript (ES6+)

**Automation:**
- Python 3.11
- BeautifulSoup4 (HTML parsing)
- Requests (HTTP client)

**Server:**
- Python HTTP Server (built-in)

---

## 📝 Usage Examples

### Manual Content Update

Edit `index.html` directly or run the automation agent.

### Scheduled Updates

Set up Windows Task Scheduler to run `run_automation.bat`:
- **Daily** at 6 AM - Fresh content every morning
- **Hourly** - Always up-to-date
- **Weekly** - Moderate refresh rate

### Custom Data Source

Modify `automation_agent.py`:
```python
self.source_url = "https://your-custom-source.com"
```

---

## 🌐 Server Commands

### Start Server (Port 8080)
```bash
cd E:\sloan-review-landing
"E:\Python\Python311\python.exe" -m http.server 8080
```

### Start Server (Custom Port)
```bash
"E:\Python\Python311\python.exe" -m http.server 3000
```

### Background Server
```bash
start "MIT Sloan Server" "E:\Python\Python311\python.exe" -m http.server 8080
```

### Stop Server
Press `Ctrl+C` in the terminal running the server

Or find and kill the process:
```bash
tasklist | findstr python
taskkill /PID <process_id> /F
```

---

## 🔄 Automation Workflow

```
1. Run automation_agent.py
   ↓
2. Fetch MIT Sloan Review
   ↓
3. Parse articles (or use fallback)
   ↓
4. Extract metadata (title, author, etc.)
   ↓
5. Update index.html
   ↓
6. Save to data_cache.json
   ↓
7. Success! Refresh browser to see changes
```

---

## 📦 Dependencies

**Python Packages:**
```
requests
beautifulsoup4
lxml
```

**Installation:**
```bash
"E:\Python\Python311\python.exe" -m pip install requests beautifulsoup4 lxml
```

---

## 🎯 Next Steps

### Enhance Automation
- Add more data sources (Harvard Business Review, McKinsey, etc.)
- Implement AI-powered summarization
- Add sentiment analysis
- Trending topic detection

### Add Features
- Search functionality
- Article detail pages
- Category pages
- Comments system
- Social sharing

### Deploy Online
- Netlify / Vercel deployment
- Custom domain
- SSL certificate
- CDN integration

---

## 🐛 Troubleshooting

### Port Already in Use
If port 8080 is taken:
```bash
"E:\Python\Python311\python.exe" -m http.server 8081
```

### Python Not Found
Use full path:
```bash
"E:\Python\Python311\python.exe" automation_agent.py
```

### Module Not Found
Install dependencies:
```bash
"E:\Python\Python311\python.exe" -m pip install requests beautifulsoup4 lxml
```

### Page Not Updating
1. Run automation agent: `run_automation.bat`
2. Hard refresh browser: `Ctrl + F5`

---

## 📄 License

Created as a prototype. Free to use and modify.

---

## 🙏 Credits

- **Design Inspiration**: MIT Sloan Management Review
- **Images**: Unsplash, Pravatar
- **Fonts**: Google Fonts (Inter)
- **Built with**: Claude Code TORQ Console

---

## 📧 Support

For issues or questions, check the automation agent logs or review the code comments.

---

**Built with ❤️ using Claude Code**

Last Updated: October 16, 2025
Version: 1.0.0
