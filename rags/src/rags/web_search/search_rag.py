from typing import List
from src.rags.web_search.search_engine import SearchEngine
from src.rags.web_search.search_params import SearchParams
from src.rags.web_search.search_result import SearchResult
from src.rags.web_search.web_scraper import WebScraper

class SearchRAG:
    """Main class for performing search and retrieval."""

    def __init__(self, search_engine: SearchEngine, web_scraper: WebScraper):
        self.search_engine = search_engine
        self.web_scraper = web_scraper

    async def search_and_retrieve(self, params: SearchParams) -> List[SearchResult]:
        """Performs a search, scrapes the results, and returns parsed data."""
        search_results = await self.search_engine.search(params)
        parsed_results = await self.web_scraper.scrape(search_results)
        return parsed_results
