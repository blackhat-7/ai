import asyncio
import traceback
import httpx
from playwright.async_api import async_playwright
from crawl4ai import AsyncWebCrawler

from typing import List, Optional, Type
from pydantic import BaseModel, ConfigDict, Field
from src.rags.web_search.search_result import SearchResult
from src.rags.web_search.html_parser import HTMLParser
from src.rags.web_search.config import SearchConfig
import asyncpraw

class WebScraper(BaseModel):
    """Handles fetching and parsing of web pages."""
    config: SearchConfig
    html_parser: HTMLParser
    reddit_client: Optional[asyncpraw.Reddit] = None
    static_websites: List[str] = Field(default=[])
    reddit_prefix: str = Field(default="https://www.reddit.com")

    model_config = ConfigDict(arbitrary_types_allowed=True)

    async def scrape(self, search_results: List[SearchResult], http_async_client: Optional[httpx.AsyncClient] = None) -> List[SearchResult]:
        """Scrapes a list of search results asynchronously."""
        if http_async_client is None:
            http_async_client = httpx.AsyncClient()
        tasks = [self._fetch_and_parse_page(http_async_client, result) for result in search_results]
        res = await asyncio.gather(*tasks)
        await http_async_client.aclose()
        return res

    async def _fetch_and_parse_page(self, client: httpx.AsyncClient, search_result: SearchResult) -> SearchResult:
        """Fetches a single page and parses it."""
        url_str = str(search_result.url)
        if any(site in url_str for site in self.static_websites):
            return await self._fetch_and_parse_static_page(client, search_result)
        elif url_str.startswith(self.reddit_prefix) and self.reddit_client is not None:
            return await self._fetch_and_parse_reddit_page(search_result)
        else:
            return await self._fetch_and_parse_dynamic_page(search_result)

    async def _fetch_and_parse_dynamic_page(self, search_result: SearchResult, CrawlerClass: Type[AsyncWebCrawler] = AsyncWebCrawler) -> SearchResult:
        """Fetches and parses a dynamic page using Playwright."""
        try:
            async with CrawlerClass() as crawler:
                # Run the crawler on a URL
                result = await crawler.arun(url=str(search_result.url))
                search_result.content = str(result.markdown)
                return search_result
        except Exception:
            print(f"Error fetching dynamic page {search_result.url}: {traceback.format_exc()}")
            return search_result  # Return the result unchanged in case of error

    async def _fetch_and_parse_static_page(self, client: httpx.AsyncClient, search_result: SearchResult) -> SearchResult:
        """Fetches and parses a static page using httpx."""
        headers = {"User-Agent": self.config.user_agent}
        try:
            response = await client.get(str(search_result.url), headers=headers, timeout=self.config.timeout)
            response.raise_for_status()
            return self.html_parser.parse(response.text, search_result)
        except httpx.HTTPError:
            print(f"Error fetching static page {search_result.url}: {traceback.format_exc()}")
            return search_result  # Return the result unchanged in case of error

    async def _fetch_and_parse_reddit_page(self, search_result: SearchResult) -> SearchResult:
        """Fetches and parses a Reddit page using AsyncPraw"""
        if self.reddit_client is None:
            raise Exception("Reddit client is not initialized")
        url_str = str(search_result.url)
        try:
            submission = await self.reddit_client.submission(url=url_str)
            # Removed the load call as it is not necessary
            content = f"Title: {submission.title} (Upvotes:{submission.score})\nContent: {submission.selftext}\nComments:\n"
            for i, comment in enumerate(submission.comments.list()):
                if isinstance(comment, asyncpraw.models.MoreComments):
                    continue
                content += f"{i}. (Upvotes:{comment.score}) {comment.body}\n"
            search_result.content = content
            return search_result
        except Exception:
            print(f"Error fetching Reddit page {search_result.url}: {traceback.format_exc()}")
            return search_result  # Return the result unchanged in case of error
