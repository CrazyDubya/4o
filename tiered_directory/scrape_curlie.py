"""Fetch site listings from Curlie for a given category.

Usage:
    python scrape_curlie.py [category_path]
Example:
    python scrape_curlie.py Computers/Internet/On_the_Web/Online_Communities
"""
import sys
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://curlie.org/en/"

def fetch_sites(category: str):
    url = BASE_URL + category.strip('/') + '/'
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, 'html.parser')
    sites = []
    for td in soup.select('div.title-and-desc'):
        a = td.find('a', href=True)
        if a and a['href'].startswith('http'):
            sites.append({'name': a.get_text(strip=True), 'url': a['href']})
    return sites

if __name__ == '__main__':
    category = sys.argv[1] if len(sys.argv) > 1 else 'Computers/Internet/On_the_Web/Online_Communities'
    for site in fetch_sites(category)[:10]:
        print(f"{site['name']} - {site['url']}")
