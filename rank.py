# TODO get wins, losses and draws of individual fighters

class Fighter:
    def __init__(self, data):

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

        self.ops = set()
        self.hist = list() # Timeline of fighter history
        self.record =  [self.wins,
                        self.losses,
                        self.draws]


class Fight:
    def __init__(self, data):
        self.f0 = Fighter(data.fighters[0])
        self.f1 = Fighter(data.fighters[1])

        self.winner 
        self.method
        self.date


# Create graph of fighters
        # Edges = {(u,v) | u,v elems of Vertices}
        # Vertices = {fighter | fighter in fighters}
        # fighters = set of all fighters
        # Each edge should contain the W,L,D outcome of the fight
def elo_rank(fighter, damp=400):
    w, l, d = fighter.record
    games = w+l+d

    rating = op_rating * damp*(w-l) / games

    1/(1+10**(R_b-R_a)/400) # Predict outcome of game
    rating = rating + 32(score-exp) # Update ratings