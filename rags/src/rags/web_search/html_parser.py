from abc import ABC, abstractmethod
from src.rags.web_search.search_result import SearchResult

class HTMLParser(ABC):
    """Abstract base class for HTML parsers."""

    @abstractmethod
    def parse(self, html: str, search_result: SearchResult) -> SearchResult:
        """Parses HTML content and updates the SearchResult object.

        Args:
            html: The HTML content to parse.
            search_result: The SearchResult object to update.

        Returns:
            The updated SearchResult object.
        """
        raise NotImplementedError