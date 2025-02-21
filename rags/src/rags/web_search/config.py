from pydantic import BaseModel, HttpUrl, Field

class SearchConfig(BaseModel):
    """Configuration for the search engine."""
    results_per_page: int = Field(default=10, description="Number of results per page.", ge=1)
    max_pages: int = Field(default=3, description="Maximum number of pages to scrape.", ge=1)
    user_agent: str = Field(
        default="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
        description="User agent string to use for requests."
    )
    timeout: int = Field(10, description="Timeout for requests in seconds.", ge=1)

class SearxngConfig(SearchConfig):
    """Configuration for the Searxng search engine."""
    base_url: HttpUrl = "https://searx.space/" # type: ignore