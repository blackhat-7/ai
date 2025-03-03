import asyncio
from crawl4ai import AsyncWebCrawler
import httpx
from pydantic import HttpUrl
import pytest
from unittest.mock import AsyncMock, Mock
from src.rags.web_search.web_scraper import WebScraper
from src.rags.web_search.search_result import SearchResult
from src.rags.web_search.config import SearchConfig
from src.rags.web_search.html_parser import HTMLParser
import asyncpraw

def raise_(ex):
    raise ex

@pytest.fixture
def mock_config():
    config = Mock(spec=SearchConfig)
    config.user_agent = "Test User Agent"
    config.timeout = 10
    return config

@pytest.fixture
def mock_html_parser():
    return Mock(spec=HTMLParser)

@pytest.mark.asyncio
async def test_scrape_success(mock_config, mock_html_parser):
    scraper = WebScraper(config=mock_config, html_parser=mock_html_parser)
    search_results = [
        SearchResult(url=HttpUrl("http://example.com"), title="Example", content="Example website")
    ]
    mock_response = AsyncMock()
    mock_response.status_code = 200
    mock_response.text = "<html><body>Test Content</body></html>"
    async with httpx.AsyncClient() as client:
        client.get = AsyncMock(return_value=mock_response)
        mock_html_parser.parse.return_value = SearchResult(
            url=HttpUrl("http://example.com"),
            title="Example",
            content="Parsed Content"
        )
        scraped_results = await scraper.scrape(search_results)
    assert len(scraped_results) == 1
    assert scraped_results[0].content != "Parsed Content"

@pytest.mark.asyncio
async def test_scrape_static_http_error(mock_config, mock_html_parser):
    scraper = WebScraper(config=mock_config, html_parser=mock_html_parser)
    search_results = SearchResult(url=HttpUrl("http://example.com"), title="Example", content="Example website")
    mock_response = Mock()
    mock_response.status_code = 404
    mock_response.raise_for_status.side_effect = Mock(side_effect=httpx.HTTPError("Some HTTP Error"))
    async with httpx.AsyncClient() as client:
        client.get = AsyncMock(return_value=mock_response)
        scraped_results = await scraper._fetch_and_parse_static_page(client, search_results)
    assert scraped_results.content == "Example website"
    mock_html_parser.parse.assert_not_called()

@pytest.mark.asyncio
async def test_scrape_static_page(mock_config, mock_html_parser):
    scraper = WebScraper(config=mock_config, html_parser=mock_html_parser, static_websites=["example.com"])
    search_results = [
        SearchResult(url=HttpUrl("http://example.com"), title="Example", content="Example website")
    ]
    mock_html_parser.parse.return_value = SearchResult(
        url=HttpUrl("http://example.com"),
        title="Example",
        content="Parsed Content"
    )
    scraped_results = await scraper.scrape(search_results)
    assert len(scraped_results) == 1
    assert scraped_results[0].content == "Parsed Content"
    mock_html_parser.parse.assert_called_once()

@pytest.mark.asyncio
async def test_scrape_reddit_page(mock_config, mock_html_parser):
    reddit_client = Mock(spec=asyncpraw.Reddit)
    submission = Mock(
        title="Example Reddit Post",
        score=100,
        selftext="Example selftext",
        comments=Mock(list=Mock(return_value=[
            Mock(score=10, body="Comment 1"),
            Mock(score=5, body="Comment 2")
        ]))
    )
    reddit_client.submission = AsyncMock(return_value=submission)
    scraper = WebScraper(config=mock_config, html_parser=mock_html_parser, reddit_client=reddit_client)
    search_results = [
        SearchResult(url=HttpUrl("https://www.reddit.com/r/example/comments/123"), title="Example", content="Example website")
    ]
    scraped_results = await scraper.scrape(search_results)
    assert len(scraped_results) == 1
    assert scraped_results[0].content == "Title: Example Reddit Post (Upvotes:100)\nContent: Example selftext\nComments:\n0. (Upvotes:10) Comment 1\n1. (Upvotes:5) Comment 2\n"
    mock_html_parser.parse.assert_not_called()
