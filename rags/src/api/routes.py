import os
import json
import datetime
import asyncpraw
from fastapi import APIRouter, Query
from typing import Dict, List, Optional
from dotenv import load_dotenv
from pydantic import HttpUrl

from src.rags.football.fbref import FbrefFetcher, TournamentEnum
from src.rags.web_search.search_rag import SearchRAG
from src.rags.web_search.searxng_search_engine import SearxngSearchEngine
from src.rags.web_search.web_scraper import WebScraper
from src.rags.web_search.basic_html_parser import BasicHTMLParser
from src.rags.web_search.config import SearxngConfig
from src.rags.web_search.search_params import SearchParams, SearchTimeRange

load_dotenv()


football_client = FbrefFetcher()

# Initialize SearchRAG components
searxng_config = SearxngConfig(
    base_url=HttpUrl("http://100.109.37.59:8181/"),  # Replace with your Searxng base URL if needed
    results_per_page=5,
    max_pages=1,
    timeout=10,
)
reddit_client = asyncpraw.Reddit(
        client_id=str(os.environ["REDDIT_CLIENT_ID"]),
        client_secret=str(os.environ["REDDIT_CLIENT_SECRET"]),
        user_agent="ChangeMeClient/0.1 by Lusion7",
    )
search_engine = SearxngSearchEngine(searxng_config)
html_parser = BasicHTMLParser()
web_scraper = WebScraper(config=searxng_config, html_parser=html_parser, reddit_client=reddit_client)
search_rag = SearchRAG(search_engine, web_scraper)


def register_routes(router: APIRouter):
    router.add_api_route("/football/matches", football_get_matches, methods=["GET"])
    router.add_api_route("/web_search", web_search_get, methods=["GET"])


async def football_get_matches(tournaments: List[str] = Query(...), start_date: datetime.datetime = Query(...)) -> Dict:
    """
    Fetch matches for the given tournaments.
    """
    global football_client
    tournaments_enums = [TournamentEnum.from_str(t) for t in tournaments]
    data = football_client.get_matches(tournaments_enums, start_date=start_date)
    return {"matches": data}


async def web_search_get(
    query: str = Query(...),
    num_results: int = Query(default=5),
    time_range: Optional[str] = Query(default=None),
    website: Optional[str] = Query(default=None),
) -> Dict:
    """
    Perform web search using SearchRAG.
    """
    search_time_range = None
    if time_range:
        search_time_range = SearchTimeRange(time_range)

    params = SearchParams(
        query=query,
        num_results=num_results,
        time_range=search_time_range,
        website=website,
    )
    results = await search_rag.search_and_retrieve(params)
    res = {"results": [result.__dict__ for result in results]}
    # print(f"search api results {json.dumps(res, indent=4, default=str)}")
    return res
