import asyncio
import os
import asyncpraw
from pydantic import HttpUrl
from dotenv import load_dotenv

from src.rags.web_search.search_rag import SearchRAG
from src.rags.web_search.searxng_search_engine import SearxngSearchEngine
from src.rags.web_search.search_params import SearchParams, SearchTimeRange
from src.rags.web_search.web_scraper import WebScraper
from src.rags.web_search.basic_html_parser import BasicHTMLParser
from src.rags.web_search.config import SearxngConfig

load_dotenv()

async def main() -> None:
    """Example usage of the SearchRAG class."""
    # 1. Configure the search engine
    config = SearxngConfig(
        base_url=HttpUrl("http://100.109.37.59:8181/"),
        results_per_page=10,
        max_pages=2,
        timeout=15
    )

    # 2. Create instances of the components
    reddit_client = asyncpraw.Reddit(
        client_id=str(os.environ["REDDIT_CLIENT_ID"]),
        client_secret=str(os.environ["REDDIT_CLIENT_SECRET"]),
        user_agent="ChangeMeClient/0.1 by Lusion7",
    )
    search_engine = SearxngSearchEngine(config)
    html_parser = BasicHTMLParser()
    web_scraper = WebScraper(config=config, html_parser=html_parser, reddit_client=reddit_client)
    search_rag = SearchRAG(search_engine, web_scraper)

    # 3. Define search parameters
    # http://localhost:8080/search?q=python%20asynchronous%20programming&language=auto&time_range=&safesearch=0&categories=general

    search_params = SearchParams(
        query="python asynchronous programming",
        website="reddit.com",  # Optional
        num_results=1,
        time_range=SearchTimeRange.Month,
    )

    # 4. Perform the search and retrieve parsed results
    results = await search_rag.search_and_retrieve(search_params)
    print(len(results))
    await reddit_client.close()

    # 5. Process the results
    for result in results:
        print(f"Title: {result.title}")
        print(f"URL: {result.url}")
        print(f"Content: {result.content}...")  # Print first 200 characters of content
        print("-" * 20)

if __name__ == "__main__":
    asyncio.run(main())
