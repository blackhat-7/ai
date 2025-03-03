# from src.rags.football.fbref import FbrefFetcher, TournamentEnum

# def test_fetcher():
#     fetcher = FbrefFetcher()
#     matches = fetcher.get_matches(
#         tournaments=[TournamentEnum.La_Liga],
#     )
#     assert len(matches) == 1
#     assert list(matches.keys())[0] == TournamentEnum.La_Liga
#     assert len(matches[TournamentEnum.La_Liga]) > 0

#     print(matches)