# Build notes

## Build 2: Trend Scraping

**Built:** Google Trends scraper with `BaseScraper` ABC so new sources (Reddit, etc.) plug in as subclasses.

**Key decisions:**
- Google Trends first — Reddit API registration was down
- One file per scraper class for clean separation
- Single `related_queries()` call per niche instead of per keyword to reduce API calls

**Bugs caught by exploring data in REPL:**
- Rising queries return garbage ("godzilla foe" for "side hustle") → added word-match filter
- `timeframe="now 7-d"` returns hourly, not daily → `iloc[-1]` was one hour's data, fixed to `iloc[-24:].mean()`
- `trending_searches()` returns 404 consistently — logged, not blocking

**To improve:**
- Normalize rising scores vs interest scores (different units)
- Language filter for non-English results
- Add Reddit scraper when API access available