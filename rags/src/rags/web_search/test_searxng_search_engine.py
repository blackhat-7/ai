import pytest
from unittest.mock import AsyncMock, MagicMock
from src.rags.web_search.searxng_search_engine import SearxngSearchEngine
from src.rags.web_search.search_params import SearchParams
from src.rags.web_search.search_result import SearchResult
from src.rags.web_search.config import SearxngConfig
import httpx
from pydantic import HttpUrl

@pytest.fixture
def mock_config():
    config = MagicMock(spec=SearxngConfig)
    config.base_url = "http://searx.space/"
    config.results_per_page = 10
    config.max_pages = 2
    config.timeout = 10
    config.user_agent = "Test User Agent"
    return config

@pytest.mark.asyncio
async def test_search_success(mock_config):
    search_engine = SearxngSearchEngine(config=mock_config)
    search_params = SearchParams(query="test", num_results=10)
    
    mock_client = AsyncMock()
    mock_response = AsyncMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "results": [
            {"url": "http://example.com", "title": "Example", "content": "Example content"}
        ]
    }
    mock_client.post.return_value = mock_response
    
    search_engine._fetch_page = AsyncMock(return_value=[
        SearchResult(url=HttpUrl("http://example.com"), title="Example", content="Example content")
    ])
    
    results = await search_engine.search(search_params)
    assert len(results) == 2
    assert results[0].url == HttpUrl("http://example.com")
    assert results[0].title == "Example"
    assert results[0].content == "Example content"

@pytest.mark.asyncio
async def test_search_http_error(mock_config):
    search_engine = SearxngSearchEngine(config=mock_config)
    search_params = SearchParams(query="test", num_results=10)
    
    mock_client = AsyncMock()
    mock_response = AsyncMock()
    mock_response.status_code = 500
    mock_response.raise_for_status.side_effect = httpx.HTTPError("Server Error")
    mock_client.post.return_value = mock_response
    
    search_engine._fetch_page = AsyncMock(side_effect=httpx.HTTPError("Server Error"))
    
    with pytest.raises(httpx.HTTPError):
        await search_engine.search(search_params)