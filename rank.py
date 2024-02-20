# TODO get wins, losses and draws of individual fighters

class Fighter:
    def __init__(self, data):
        self.data = dict()

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
        self.f1 = Fighter()
        self.f2 = Fighter()

        self.winner 
        self.method
        self.date

def elo_rank(fighter, damp=400):
    w, l, d = fighter.record
    games = w+l+d

    rating = op_rating * damp*(w-l) / games

    1/(1+10**(R_b-R_a)/400)# Predict outcome of game
    rating = rating + 32(score-exp) # Update ratings