"""Demonstrate simple tier assignment for Curlie category sites.

Usage:
    python build_tiers.py [category_path]

The first site is marked S-tier, then A/B/C/D tiers get 2/3/4/5 sites
respectively, with the remainder assigned to F-tier. This is a placeholder
algorithm until proper ranking metrics are integrated.
"""
import sys
from scrape_curlie import fetch_sites

TIER_COUNTS = [
    ("S", 1),
    ("A", 2),
    ("B", 3),
    ("C", 4),
    ("D", 5),
]


def assign_tiers(sites):
    tiers = {}
    idx = 0
    for tier, count in TIER_COUNTS:
        if idx >= len(sites):
            break
        tiers[tier] = sites[idx:idx + count]
        idx += count
    if idx < len(sites):
        tiers["F"] = sites[idx:]
    return tiers


def main():
    category = (
        sys.argv[1]
        if len(sys.argv) > 1
        else "Computers/Internet/On_the_Web/Online_Communities"
    )
    sites = fetch_sites(category)
    tiers = assign_tiers(sites)
    for tier in ["S", "A", "B", "C", "D", "F"]:
        for site in tiers.get(tier, []):
            print(f"{tier}: {site['name']} - {site['url']}")


if __name__ == "__main__":
    main()
