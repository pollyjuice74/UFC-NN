from nba_api.live.nba.endpoints import scoreboard

# Today's Score Board
games = scoreboard.ScoreBoard()

# json
print(games.get_json())

# dictionary
print(games.get_dict())