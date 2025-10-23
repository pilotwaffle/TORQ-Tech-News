#!/usr/bin/env python3
"""Add route for populate_main_articles.js to app.py"""

with open('app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find the line with @app.route('/populate_ai_section.js')
# and add the new route after its function definition
new_route = """@app.route('/populate_main_articles.js')
def serve_main_articles_js():
    \"\"\"Serve main articles population JavaScript\"\"\"
    return send_from_directory('.', 'populate_main_articles.js')

"""

insert_index = None
for i, line in enumerate(lines):
    if "@app.route('/data_cache.json')" in line:
        insert_index = i
        break

if insert_index:
    lines.insert(insert_index, new_route)

    with open('app.py', 'w', encoding='utf-8') as f:
        f.writelines(lines)

    print("[OK] Added populate_main_articles.js route to app.py")
else:
    print("[ERROR] Could not find insertion point in app.py")
