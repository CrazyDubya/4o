# Tiered Web Directory

This prototype aims to explore data sources and scraping approaches for building a tiered directory of the web.  

## Goal
Create a categorical and sub‑categorical system that ranks prominent websites into S/A/B/C/D/F tiers.  

## Approach
1. **Collect candidate sites** for each category using open data sources.  
2. **Gather ranking signals** (traffic, backlinks, etc.) from available APIs.  
3. **Assign tiers** based on thresholds or combined scores.  
4. **Expose results** as a browsable directory.

## Candidate Data Sources
| Source | Type | Pros | Cons |
|-------|------|------|------|
| [Curlie](https://curlie.org) | curated directory | hierarchical categories, easy to scrape | manual curation, inconsistent updates |
| [Wikipedia](https://www.wikipedia.org) | lists & categories | open API, many niche lists | may be incomplete, requires filtering |
| [Tranco](https://tranco-list.eu) | top sites list | reproducible ranking of the top 1M domains | no categorization |
| [Open PageRank](https://www.domcop.com/openpagerank/) | API | provides rank metric for domains | rate limits, API key for higher usage |
| [Common Crawl](https://commoncrawl.org) | massive crawl data | free, comprehensive | large data volume, needs processing |

Commercial APIs (e.g., SimilarWeb, Ahrefs, Moz) could supplement ranking signals but often require paid access.

## Tiering Strategy
Combine multiple metrics (e.g., Tranco rank percentile, PageRank score) to compute a composite score.  
Suggested thresholds:

- **S-tier**: top 0.1%
- **A-tier**: next 0.9%
- **B-tier**: next 4%
- **C-tier**: next 15%
- **D-tier**: next 30%
- **F-tier**: remainder

These thresholds are illustrative; they should be adjusted based on the distribution of ranking metrics.

## Demo
Run a quick prototype that fetches a Curlie category and assigns provisional tiers:

```bash
python build_tiers.py Computers/Internet/On_the_Web/Online_Communities | head
```

The script marks the first few sites as S/A/B/C/D tiers and places the remainder in F-tier. It serves only as an example until real ranking signals are incorporated.

## Next Steps
- Expand scraping to additional sources.
- Store results in structured format (JSON/CSV/DB).
- Build a small web interface to browse tiers by category.
