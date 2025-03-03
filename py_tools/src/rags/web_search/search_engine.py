from abc import ABC, abstractmethod
from typing import List
from src.rags.web_search.search_params import SearchParams
from src.rags.web_search.search_result import SearchResult
from src.rags.web_search.config import SearchConfig

class SearchEngine(ABC):
    """Abstract base class for search engines."""

    def __init__(self, config: SearchConfig):
        self.config = config

    @abstractmethod
    async def search(self, params: SearchParams) -> List[SearchResult]:
        """
        Performs a search using the given parameters.

        Args:
            params: The search parameters.

        Returns:
            A list of SearchResult objects.
        """
        raise NotImplementedError