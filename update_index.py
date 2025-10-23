#!/usr/bin/env python3
"""Update index.html to add articles-grid ID and populate script"""

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Add ID to articles-grid div (only the first occurrence, not the AI one)
content = content.replace(
    '    <div class="articles-grid">\n     <!-- Article 1 -->',
    '    <div class="articles-grid" id="articles-grid">\n     <!-- Article 1 -->'
)

# Add populate_main_articles.js script after populate_ai_section.js
content = content.replace(
    '  <script src="populate_ai_section.js">\n  </script>',
    '  <script src="populate_ai_section.js">\n  </script>\n  <script src="populate_main_articles.js">\n  </script>'
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("[OK] Updated index.html")
print("   - Added id='articles-grid' to main articles container")
print("   - Added populate_main_articles.js script tag")
