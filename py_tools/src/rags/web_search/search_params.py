from enum import Enum
from pydantic import BaseModel, Field
from typing import List, Optional

class SearchTimeRange(str, Enum):
    Day = "day"
    Month = "month"
    Year = "year"

class SearchParams(BaseModel):
    """Parameters for a search query."""
    query: str = Field(..., description="The search query string.")
    website: Optional[str] = Field(default=None, description="Specific website to search within.")
    num_results: int = Field(default=10, description="Desired number of search results.", ge=1)
    time_range: Optional[SearchTimeRange] = Field(default=None, description="Time range for the search (e.g., day, month, year).")
