from pydantic import HttpUrl
from src.rags.web_search.basic_html_parser import BasicHTMLParser
from src.rags.web_search.search_result import SearchResult

def test_parse():
    html_content = "<p>Hello, world!</p><p>This is a test.</p>"
    search_result = SearchResult(url=HttpUrl("http://example.com"), title="Example", content="")
    parser = BasicHTMLParser()
    result = parser.parse(html_content, search_result)
    assert result.content == "Hello, world! This is a test."

def test_parse_no_paragraphs():
    html_content = "<div>No paragraphs here.</div>"
    search_result = SearchResult(url=HttpUrl("http://example.com"), title="Example", content="")
    parser = BasicHTMLParser()
    result = parser.parse(html_content, search_result)
    assert result.content == ""

def test_parse_multiple_paragraphs():
    html_content = "<p>First paragraph.</p><p>Second paragraph.</p><p>Third paragraph.</p>"
    search_result = SearchResult(url=HttpUrl("http://example.com"), title="Example", content="")
    parser = BasicHTMLParser()
    result = parser.parse(html_content, search_result)
    assert result.content == "First paragraph. Second paragraph. Third paragraph."