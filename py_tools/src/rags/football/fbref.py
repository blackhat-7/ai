import datetime
import pandas as pd
from enum import Enum
from abc import ABC, abstractmethod
from pydantic import BaseModel, PrivateAttr
from typing import List, Dict, Optional


class TournamentEnum(Enum):
    Champions_League = 8
    Premier_League = 9
    Serie_A = 11
    La_Liga = 12
    Ligue_1 = 13
    Bundesliga = 20
    Saudi_Professional_League = 70
    Indian_Super_League = 82

    @classmethod
    def from_str(cls, tournament_str: str) -> "TournamentEnum":
        for tournament in TournamentEnum:
            if tournament.name.lower() == tournament_str.lower():
                return tournament
        raise ValueError(f"Invalid tournament name: {tournament_str}")


class Team(BaseModel):
    name: str


class Score(BaseModel):
    home: int
    away: int

    @classmethod
    def from_str(cls, score_str: str):
        home, away = score_str.split("–")
        return Score(home=int(home), away=int(away))


class Match(BaseModel):
    week: int
    date_time: datetime.datetime
    home: Team
    away: Team
    score: Optional[Score]
    home_xg: Optional[float]
    away_xg: Optional[float]


class FootballFetcher(ABC):
    def get_matches(
        self,
        tournaments: List[TournamentEnum],
        start_date: Optional[datetime.datetime] = None,
        end_date: Optional[datetime.datetime] = None,
    ) -> Dict[TournamentEnum, List[Match]]:
        raise NotImplementedError


class FbrefFetcher(FootballFetcher):
    _season_start_month: int = PrivateAttr()

    def model_post_init(self):
        self._season_start_month = 8

    def get_matches(
        self,
        tournaments: List[TournamentEnum],
        start_date: Optional[datetime.datetime] = None,
        end_date: Optional[datetime.datetime] = None,
    ) -> Dict[TournamentEnum, List[Match]]:
        """
        """
        now = datetime.datetime.now()
        if start_date is None:
            start_date = now
        if end_date is None:
            end_date = now
        start_strf = start_date.strftime("%Y-%m-%d")
        end_strf = end_date.strftime("%Y-%m-%d")

        matches: Dict[TournamentEnum, List[Match]] = {}
        if start_date.year < now.year:
            raise NotImplementedError

        if end_date.year == now.year:
            for t in tournaments:
                t_matches = pd.read_html(
                    f"https://fbref.com/en/comps/{t.value}/schedule/"
                )[0]
                t_matches_lst = self.parse_matches(t_matches, start_strf, end_strf)
                matches[t] = t_matches_lst

        return matches

    @staticmethod
    def parse_matches(
        matches_df: pd.DataFrame, start_strf: str, end_strf: str
    ) -> List[Match]:
        matches_df = matches_df[
            (matches_df["Date"] >= start_strf) & (matches_df["Date"] <= end_strf)
        ]
        matches: List[Match] = []
        for m in matches_df.to_dict("records"):
            match = Match(
                week=int(m["Wk"]),
                date_time=datetime.datetime.strptime(
                    m["Date"] + " " + m["Time"], "%Y-%m-%d %H:%M"
                ),
                home=Team(name=m["Home"]),
                away=Team(name=m["Away"]),
                score=Score.from_str(m["Score"]) if not pd.isna(m["Score"]) else None,
                home_xg=float(m["xG"]) if not pd.isna(m["xG"]) else None,
                away_xg=float(m["xG.1"]) if not pd.isna(m["xG.1"]) else None,
            )
            matches.append(match)
        return matches




"""
https://fbref.com/en/comps/12/schedule/La-Liga-Scores-and-Fixtures
https://fbref.com/en/comps/12/2023-2024/schedule/2023-2024-La-Liga-Scores-and-Fixtures
https://fbref.com/en/comps/9/schedule/Premier-League-Scores-and-Fixtures
https://fbref.com/en/comps/20/schedule/Bundesliga-Scores-and-Fixtures
https://fbref.com/en/comps/11/schedule/Serie-A-Scores-and-Fixtures
https://fbref.com/en/comps/13/schedule/Ligue-1-Scores-and-Fixtures
https://fbref.com/en/comps/82/schedule/Indian-Super-League-Scores-and-Fixtures
https://fbref.com/en/comps/70/schedule/Saudi-Professional-League-Scores-and-Fixtures
https://fbref.com/en/comps/8/schedule/Champions-League-Scores-and-Fixtures
"""