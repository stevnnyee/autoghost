from abc import ABC, abstractmethod


class BaseScraper(ABC):

    @abstractmethod
    def scrape(self):
        """Fetch raw data from the source."""
        pass

    @abstractmethod
    def parse(self, raw_data):
        """Parse raw data into a list of trend dicts with keys: title, source, niche, score."""
        pass

    @abstractmethod
    def score(self, trends):
        """Score and rank parsed trends. Return sorted list."""
        pass

    def run(self):
        """Execute the full scraping pipeline."""
        raw_data = self.scrape()
        trends = self.parse(raw_data)
        scores = self.score(trends)
        return scores