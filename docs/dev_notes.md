# Build notes

## Build 1: Foundation & Setup

**Built:** Project skeleton with config management and database models.

**What was created:**
- `configs/config.py` — centralized config loading API keys from `.env` via `python-dotenv`
- `core/database.py` — SQLAlchemy models: Account, Trend, Video, Analytics, TrendingSound
- `requirements.txt` — project dependencies
- `.env.sample` — API key template
- `.gitignore` — sensitive data exclusion
- `data/` directory for generated content

**Key decisions:**
- SQLite for database (simple, no setup, upgrade to PostgreSQL later if needed)
- SQLAlchemy ORM over raw SQL for cleaner model definitions
- Flat project structure (`core/`, `configs/`) at root level instead of nested under `autoghost/` package

---

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