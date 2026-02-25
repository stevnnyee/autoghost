import time
import logging

from pytrends.request import TrendReq
from scrapers.base_scraper import BaseScraper

logging.basicConfig(level=logging.INFO)

NICHE_KEYWORDS = {
    "finance": [
        "side hustle",
        "passive income",
        "investing",
        "budgeting",
        "money tips",
    ],
    "productivity": [
        "productivity tips",
        "time management",
        "morning routine",
        "habits",
        "focus",
    ],
    "entrepreneur": [
        "startup",
        "online business",
        "freelancing",
        "marketing tips",
        "dropshipping",
    ],
}


class GoogleTrendsScraper(BaseScraper):
    def __init__(self):
        self.pytrends = TrendReq()

    def scrape(self):
        raw_data = {}

        for niche, keywords in NICHE_KEYWORDS.items():
            self.pytrends.build_payload(keywords, timeframe="now 7-d")
            interest = self.pytrends.interest_over_time()
            time.sleep(2)

            related = {}
            all_related = self.pytrends.related_queries()
            for kw in keywords:
                try:
                    related[kw] = all_related[kw]["rising"]
                except (KeyError, TypeError) as e:
                    logging.warning(f"No rising queries for '{kw}': {e}")
                    related[kw] = None
            time.sleep(2)

            raw_data[niche] = {"interest": interest, "related": related}

        try:
            trending = self.pytrends.trending_searches(pn="united_states")
            raw_data["_trending"] = trending
        except Exception as e:
            logging.warning(f"Failed to fetch trending searches: {e}")
            raw_data["_trending"] = None
        return raw_data

    def parse(self, raw_data):
        trends = []

        trending_df = raw_data.pop("_trending", None)
        if trending_df is not None and not trending_df.empty:
            for _, row in trending_df.iterrows():
                trends.append(
                    {
                        "title": row[0],
                        "source": "google_trends_realtime",
                        "niche": "general",
                        "score": 100.0,
                    }
                )

        for niche, data in raw_data.items():
            for kw, rising_df in data["related"].items():
                if rising_df is None or rising_df.empty:
                    continue
                for _, row in rising_df.iterrows():
                    query = row["query"].lower()
                    if not any(word in query for word in kw.lower().split()):
                        continue
                    trends.append(
                        {
                            "title": row["query"],
                            "source": "google_trends",
                            "niche": niche,
                            "score": float(row["value"]),
                        }
                    )

            interest_df = data["interest"]
            if interest_df.empty:
                continue
            latest = interest_df.iloc[-24:].mean().drop("isPartial", errors="ignore")
            for kw, value in latest.items():
                if value > 50:
                    trends.append(
                        {
                            "title": kw,
                            "source": "google_trends",
                            "niche": niche,
                            "score": float(value),
                        }
                    )

        return trends

    def score(self, trends):
        seen = set()
        unique = []
        for t in trends:
            if t["title"].lower() not in seen:
                seen.add(t["title"].lower())
                unique.append(t)
        return sorted(unique, key=lambda t: t["score"], reverse=True)


if __name__ == "__main__":
    scraper = GoogleTrendsScraper()
    results = scraper.run()
    for t in results[:20]:
        print(f"[{t['niche']}] {t['title']} (score: {t['score']})")
