from pydantic import BaseModel, HttpUrl, Field

class SearchResult(BaseModel):
    """Represents a single search result."""
    url: HttpUrl = Field(..., description="URL of the search result.")
    title: str = Field(..., description="Title of the page.")
    content: str = Field(..., description="Content of the page (e.g., extracted text).")