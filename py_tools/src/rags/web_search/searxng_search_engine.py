import asyncio
import httpx
from bs4 import BeautifulSoup
from datetime import date, timedelta
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, HttpUrl

from src.rags.web_search.search_engine import SearchEngine
from src.rags.web_search.search_params import SearchParams
from src.rags.web_search.search_result import SearchResult
from src.rags.web_search.config import SearxngConfig

class SearxngResult(BaseModel):
    url: str
    title: str
    content: str

class SearxngSearchEngine(SearchEngine):
    """Searxng implementation of the SearchEngine."""
    config: SearxngConfig

    async def _fetch_page(self, client: httpx.AsyncClient, url: str, data: Dict[str, Any]) -> List[SearxngResult]:
        """Fetches the content of a single page."""
        headers = {"User-Agent": self.config.user_agent}
        response = await client.post(url, headers=headers, data=data, timeout=self.config.timeout)
        response.raise_for_status()
        return [SearxngResult.model_validate(r) for r in response.json()['results']]

    def _parse_search_results(self, searxng_results: List[SearxngResult]) -> List[SearchResult]:
        """Parses the search results page HTML."""
        return [
            SearchResult(
                url=HttpUrl(result.url),
                title=result.title,
                content=result.content,
            ) for result in searxng_results
        ]


    async def search(self, params: SearchParams) -> List[SearchResult]:
        """Searches using Searxng and returns parsed results."""
        print(f"Searching for '{params.query}' on {self.config.base_url}")
        results: List[SearchResult] = []
        tasks = []

        async with httpx.AsyncClient() as client:
            for page_num in range(self.config.max_pages):
                # Construct the search URL for Searxng
                search_url = f"{self.config.base_url}search"

                # Build the query parameters
                data = {
                    "q": params.query,
                    "format": "json",  # Request HTML format for easier parsing
                    "pageno": str(page_num + 1),
                    "safesearch": 0,
                    "language": "auto",
                    "category_general": 1,
                }

                # Add optional parameters
                if params.website:
                    data["q"] += f" site:{params.website}"

                if params.time_range is not None:
                    data["time_range"] = params.time_range.value

                # Fetch the page asynchronously
                tasks.append(self._fetch_page(client, search_url, data=data))

            pages = await asyncio.gather(*tasks)

            for page in pages:
                page_results = self._parse_search_results(page)
                results.extend(page_results)

        return results[:params.num_results]
