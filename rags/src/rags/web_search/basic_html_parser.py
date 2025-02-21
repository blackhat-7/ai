from bs4 import BeautifulSoup
from src.rags.web_search.html_parser import HTMLParser
from src.rags.web_search.search_result import SearchResult

class BasicHTMLParser(HTMLParser):
    """A basic HTML parser that extracts text content."""

    def parse(self, html: str, search_result: SearchResult) -> SearchResult:
        """Parses HTML and extracts text content."""
        soup = BeautifulSoup(html, "html.parser")

        # Extract all text from <p> tags as a basic example
        text_content = " ".join([p.get_text() for p in soup.find_all("p")])

        search_result.content = text_content
        return search_result