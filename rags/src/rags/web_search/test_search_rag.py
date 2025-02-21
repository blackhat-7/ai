import asyncio
import pytest
from unittest.mock import AsyncMock, MagicMock
from src.rags.web_search.search_rag import SearchRAG
from src.rags.web_search.search_engine import SearchEngine
from src.rags.web_search.web_scraper import WebScraper
from src.rags.web_search.search_params import SearchParams
from src.rags.web_search.search_result import SearchResult
from pydantic import HttpUrl

@pytest.fixture
def mock_search_engine():
    search_engine = MagicMock(spec=SearchEngine)
    search_engine.search = AsyncMock(return_value=[
        SearchResult(url=HttpUrl("http://example.com"), title="Example", content="Example website")
    ])
    return search_engine

@pytest.fixture
def mock_web_scraper():
    web_scraper = MagicMock(spec=WebScraper)
    web_scraper.scrape = AsyncMock(return_value=[
        SearchResult(url=HttpUrl("http://example.com"), title="Example", content="Parsed Content")
    ])
    return web_scraper

@pytest.fixture
def mock_search_params():
    return SearchParams(query="test", num_results=10)

@pytest.mark.asyncio
async def test_search_and_retrieve(mock_search_engine, mock_web_scraper, mock_search_params):
    search_rag = SearchRAG(search_engine=mock_search_engine, web_scraper=mock_web_scraper)
    results = await search_rag.search_and_retrieve(mock_search_params)
    assert len(results) == 1
    assert results[0].url == HttpUrl("http://example.com")
    assert results[0].title == "Example"
    assert results[0].content == "Parsed Content"
    mock_search_engine.search.assert_called_once_with(mock_search_params)
    mock_web_scraper.scrape.assert_called_once_with([
        SearchResult(url=HttpUrl("http://example.com"), title="Example", content="Example website")
    ])