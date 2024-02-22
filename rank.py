# TODO get wins, losses and draws of individual fighters

class Fighter:
    def __init__(self, data, base_rating=1500):

        # Data
        ###############################################
        self.data = data ### dict()

        self.name = data.get('name', '')  # Fighter's name
        self.wins = data.get('wins', 0)  # Total number of wins
        self.losses = data.get('losses', 0)  # Total number of losses
        self.draws = data.get('draws', 0)  # Total number of draws

        self.strikes = data.get('strikes', 0)  # Total number of strikes attempted
        self.strikes_landed = data.get('strikes_landed', 0)  # Total number of strikes that landed

        self.takedowns = data.get('takedowns', 0)  # Total number of takedown attempts
        self.takedowns_landed = data.get('takedowns_landed', 0)  # Total number of successful takedowns

        # Win methods ("Submission", "KO", "Decision")
        self.win_method = data.get('win_method', {})  # Example: {"Submission": {"Rear Naked Choke": 2, "Guillotine": 1}, "KO": 5}
        ###############################################

        self.wins = 0
        self.losses = 0
        self.draws = 0

        self.rating = base_rating

        self.ops = set()
        self.hist = list() # Timeline of fighter history
        self.record =  [self.wins,
                        self.losses,
                        self.draws]


class Fight:
    def __init__(self, data, completed=False):
        self.f0 = Fighter(data.fighters[0])
        self.f1 = Fighter(data.fighters[1])

        self.winner = self.get_winner() if completed else None
        self.loser = self.get_loser() if completed else None

        self.method = None
        self.date = None


class FighterGraph:
    """
    Create graph of fighters
        fighters = set of all fighters
        Vertices = {fighter | fighter in fighters}
        Edges = {(u,v, winner_id) | u,v elems of Vertices}
        Each edge should contain the W,L,D outcome of the fight
    """
    def __init__(self, fighters):
        self.fighters = fighters #set()
        self.ranks = dict() # fighter.name: rank

        self.v = {fighter.name for fighter in self.fighters} # Vertices
        self.e = set() # Edges
        for fighter in self.fighters:
            for fight in fighter.fights:
                win_status = fight.winner if fight.winner else None
                self.e.add((fighter.name, fight.opp.name, win_status))
        
        self.calculate_ranks()

    def calculate_ranks(self):
        # Populate ranks dictionary
        for fighter in self.fighters:
            self.ranks[fighter.name] = fighter.rank

        #
        for u, v, winner_name in self.e:
            if winner_name:
                winner = u if u.name == winner_name else v if v.name == winner_name else None
                loser = v if u == winner else u

                self.update_elo_ratings(winner, loser)

            else: # Draw
                winner = None
                loser = None

            
    
    def update_ranks(self):
        # Updates already calculated ranks with new fighters adding to the data
        pass
        
    def update_elo_ratings(winner, loser, K=32):  
        """
        Input
            winner: Fighter object
            loser: Fighter object
            draw: flag
            K: damping factor
        Output
            None
        """  
        # Calculate expected scores
        exp_winner = 1 / (1 + 10 ** ((loser.rating - winner.rating) / 400)) # Predict outcome of game #rating = op_rating * damp*(w-l) / games
        exp_loser = 1 / (1 + 10 ** ((winner.rating - loser.rating) / 400))
        
        # Actual scores
        score_winner, score_loser = 1,0 
        
        # Update ratings
        winner.elo_rating = winner.rating + K * (score_winner - exp_winner)
        loser.elo_rating = loser.rating + K * (score_loser - exp_loser)



def elo_rank(fighter, damp=400):
    w, l, d = fighter.record
    games = w+l+d


