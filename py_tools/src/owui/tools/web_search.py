"""
title: Web Search using Custom Web search API
author: blackhat-7
funding_url: https://github.com/open-webui
version: 0.1
license: MIT
"""

import asyncio
from pydantic.type_adapter import P
import requests
import json
from urllib.parse import urlparse
import re
import unicodedata
from pydantic import BaseModel, Field
from typing import Callable, Any, Dict, List


class HelpFunctions:
    def __init__(self):
        pass

    def get_base_url(self, url):
        parsed_url = urlparse(url)
        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
        return base_url

    def generate_excerpt(self, content, max_length=200):
        return content[:max_length] + "..." if len(content) > max_length else content




class EventEmitter:
    def __init__(self, event_emitter: Callable[[dict], Any] = None):
        self.event_emitter = event_emitter

    async def emit(self, description="Unknown State", status="in_progress", done=False):
        if self.event_emitter:
            await self.event_emitter(
                {
                    "type": "status",
                    "data": {
                        "status": status,
                        "description": description,
                        "done": done,
                    },
                }
            )

class SearchResults(BaseModel):
    query: str
    results: List[Any]

class Tools:
    class Valves(BaseModel):
        WEB_SEARCH_API_URL: str = Field(
            default="https://example.com/search",
            description="The base URL for Search API",
        )
        NUM_RESULTS: int = Field(
            default=3,
            description="The number of Search Engine Results to Parse",
        )
        PAGE_CONTENT_WORDS_LIMIT: int = Field(
            default=5000,
            description="Limit words content for each page.",
        )
        CITATION_LINKS: bool = Field(
            default=False,
            description="If True, send custom citations with links",
        )

    def __init__(self):
        self.valves = self.Valves()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }

    async def search_web(
        self,
        queries: List[str],
        time_range: str = "",
        website: str = "",
        __event_emitter__: Callable[[dict], Any] = None,
    ) -> str:
        """
        Search for unknown knowledge, news, info, public contact info, weather, etc. Break down a complex user question into multiple queries if necessary and search the web and get the content of the relevant pages. time_range and website are optional parameters.

        :params query (required): List of Web Queries used in search engine. You may need to rephrase the query to get better results. Works better with key words instead of whole sentences.
        :params time_range (optional): The time range for the search (e.g., "day", "month" or "year"). Use this IF AND ONLY IF the user specifies in some way that he wants recent results or within a time range. In all other cases pass an empty string.
        :params website (optional): If need results of a specific website only. Use this IF AND ONLY IF the user specifies in some way that he wants results from a specific website. In all other cases pass an empty string. The website should be in the format of "www.example.com".

        :return: The content of the pages in json format.
        """
        emitter = EventEmitter(__event_emitter__)
        if not isinstance(queries, list):
            await emitter.emit(
                status="error",
                description="Invalid queries format, please provide a list of queries",
                done=True,
            )
            return json.dumps({"error": "Invalid queries format, please provide a list of queries"})

        if len(queries) > 3:
            await emitter.emit(
                status="error",
                description="Too many queries, please reduce the number of queries",
                done=True,
            )
            return json.dumps({"error": "Too many queries, please reduce the number of queries"})

        await emitter.emit(f"Initiating web search for: {' and '.join(queries)}")

        try:
            search_results = await self.search_and_scrape(queries, time_range, website)
        except Exception as e:
            await emitter.emit(
                status="error",
                description=f"Error during search: {str(e)}",
                done=True,
            )
            return json.dumps({"error": str(e)})


        await emitter.emit(f"Retrieved {len(search_results)} search results")

        processed_results: List[SearchResults] = []
        if search_results:
            try:
                processed_results = self.process_results(search_results)
            except Exception as e:
                await emitter.emit(
                    status="error",
                    description=f"Error during processing results: {str(e)}",
                    done=True,
                )
                return json.dumps({"error": str(e)})

            if self.valves.CITATION_LINKS and __event_emitter__:
                for s_results in processed_results:
                    for r in s_results.results:
                        await __event_emitter__(
                            {
                                "type": "citation",
                                "data": {
                                    "document": [r['content']],
                                    "metadata": [{"source": r['url']}],
                                    "source": {"name": r['title']},
                                },
                            }
                        )

        await emitter.emit(
            status="complete",
            description=f"Web search completed | {sum(len(r.results) for r in processed_results)} results | {len(queries)} queries",
            done=True,
        )

        # print(f"Final data to llm:\n{json.dumps(results_json, indent=4)}")
        return json.dumps([r.model_dump(mode='json') for r in processed_results], ensure_ascii=False)

    async def search_and_scrape(self, queries: List[str], time_range: str, website: str) -> List[SearchResults]:
        # Search and scrape asynchronously
        results = [self.call_search_and_scrape_query(query, time_range, website) for query in queries]
        return await asyncio.gather(*results)


    async def call_search_and_scrape_query(self, query: str, time_range: str, website: str) -> SearchResults:
        params = {
            "query": query,
            "number_of_results": self.valves.NUM_RESULTS,
        }
        if time_range:
            for tr in ['day', 'month', 'year']:
                if tr in time_range.lower():
                    params['time_range'] = tr
                    break
        else:
            params['time_range'] = None

        if website:
            params['website'] = website
        else:
            params['website'] = None

        resp = requests.get(
            self.valves.WEB_SEARCH_API_URL, params=params, headers=self.headers, timeout=120
        )
        resp.raise_for_status()
        data = resp.json()

        return SearchResults(query=query, results=data.get("results", []))

    def process_results(self, search_results: List[SearchResults]) -> List[SearchResults]:
        processor = TextProcessor()
        for r in search_results:
            for i, result in enumerate(r.results):
                r.results[i] = processor.process_search_result(
                    result,
                    self.valves.PAGE_CONTENT_WORDS_LIMIT
                )
        return search_results

class TextProcessor:
    def format_text(self, original_text):
        # soup = BeautifulSoup(original_text, "html.parser")
        # formatted_text = soup.get_text(separator=" ", strip=True)
        formatted_text = unicodedata.normalize("NFKC", original_text)
        formatted_text = re.sub(r"\s+", " ", formatted_text)
        formatted_text = formatted_text.strip()
        formatted_text = self.remove_emojis(formatted_text)
        return formatted_text

    def remove_emojis(self, text):
        return "".join(c for c in text if not unicodedata.category(c).startswith("So"))

    def process_search_result(self, result: Dict[str, str], page_content_word_limit: int) -> Dict[str, str]:
        content = self.format_text(result['content'])
        content = self.truncate_to_n_words(
            content, page_content_word_limit
        )
        result['content'] = content
        return result

    def truncate_to_n_words(self, text: str, token_limit: int):
        tokens = text.split()
        truncated_tokens = tokens[:token_limit]
        return " ".join(truncated_tokens)
