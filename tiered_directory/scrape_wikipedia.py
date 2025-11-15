"""Fetch members of a Wikipedia category via MediaWiki API.

Usage:
    python scrape_wikipedia.py [Category_Name]
Example:
    python scrape_wikipedia.py Search_engine_software
"""
import sys
import requests

API_URL = "https://en.wikipedia.org/w/api.php"

def fetch_category_members(category: str, limit: int = 20):
    params = {
        'action': 'query',
        'list': 'categorymembers',
        'cmtitle': f'Category:{category}',
        'cmlimit': limit,
        'format': 'json'
    }
    data = requests.get(API_URL, params=params, timeout=10).json()
    return [m['title'] for m in data.get('query', {}).get('categorymembers', [])]

if __name__ == '__main__':
    category = sys.argv[1] if len(sys.argv) > 1 else 'Search_engine_software'
    for title in fetch_category_members(category):
        print(title)
