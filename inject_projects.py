"""
Reads repos.json (fetched from GitHub API) and injects
a fresh project list into index.html between
<!-- PROJECTS_START --> and <!-- PROJECTS_END --> markers.

To use: add those HTML comment markers around your project
cards section in index.html, then this script replaces
the content automatically on every push.
"""
import json, re

with open('repos.json') as f:
    repos = json.load(f)

# Repos to always pin at the top (your featured work)
PINNED = [
    'real-time-ride-analytics',
    'Nifty-50-Stocks-Prediction',
    'London-Airbnb-Market-Analysis',
    'Customer-Churn-Prediction',
]

ICONS = {
    'real-time-ride-analytics': '🚀',
    'Nifty-50-Stocks-Prediction': '📈',
    'London-Airbnb-Market-Analysis': '🏠',
    'Customer-Churn-Prediction': '🔄',
}

def make_card(repo, featured=False):
    name = repo['name']
    desc = repo.get('description') or 'View on GitHub for details.'
    url  = repo['html_url']
    lang = repo.get('language') or ''
    icon = ICONS.get(name, '💡')
    star_class = 'proj-card star' if featured else 'proj-card'
    badge = '<span class="pbadge pbadge-feat">FEATURED</span>' if featured else '<span class="pbadge pbadge-gh">GITHUB</span>'
    title = name.replace('-', ' ').title()
    return f"""
    <div class="{star_class}">
      <div class="proj-header">
        <div class="proj-icon">{icon}</div>
        {badge}
      </div>
      <div class="proj-title">{title}</div>
      <p class="proj-desc">{desc}</p>
      <div class="stack"><span class="stag">{lang}</span></div>
      <a href="{url}" target="_blank" class="proj-link">View on GitHub →</a>
    </div>"""

# Sort: pinned first, then rest by update date
pinned_repos = [r for r in repos if r['name'] in PINNED]
pinned_repos.sort(key=lambda r: PINNED.index(r['name']))
other_repos  = [r for r in repos if r['name'] not in PINNED and not r.get('fork')]

cards = ''.join(make_card(r, featured=(i==0)) for i, r in enumerate(pinned_repos))
cards += ''.join(make_card(r) for r in other_repos[:2])  # add up to 2 extra

new_block = f'<!-- PROJECTS_START -->\n<div class="proj-grid">{cards}\n</div>\n<!-- PROJECTS_END -->'

with open('index.html') as f:
    html = f.read()

html = re.sub(r'<!-- PROJECTS_START -->.*?<!-- PROJECTS_END -->', new_block, html, flags=re.DOTALL)

with open('index.html', 'w') as f:
    f.write(html)

print(f"Injected {len(pinned_repos)} pinned + {min(2,len(other_repos))} extra projects.")
