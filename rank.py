# TODO get wins, losses and draws of individual fighters
import os
import json


current_directory = os.path.dirname(__file__) 
fighters_json_path = os.path.join(current_directory, 'UFCspdr', 'Fighters.json')
fights_json_path = os.path.join(current_directory, 'UFCspdr', 'Fights.json')


class Fighter:
    def __init__(self, data, base_rating=1500):

        # Data
        ###############################################

        # self.wins = data.get('wins', 0)  # Total number of wins
        # self.losses = data.get('losses', 0)  # Total number of losses
        # self.draws = data.get('draws', 0)  # Total number of draws

        # self.strikes = data.get('strikes', 0)  # Total number of strikes attempted
        # self.strikes_landed = data.get('strikes_landed', 0)  # Total number of strikes that landed

        # self.takedowns = data.get('takedowns', 0)  # Total number of takedown attempts
        # self.takedowns_landed = data.get('takedowns_landed', 0)  # Total number of successful takedowns

        # # Win methods ("Submission", "KO", "Decision")
        # self.win_method = data.get('win_method', {})  # Example: {"Submission": {"Rear Naked Choke": 2, "Guillotine": 1}, "KO": 5}
        ###############################################

        self.name = data.get('name')  # Fighter's name
        self.url = data.get('url') # Fighter's url

        self.wins = data.get('wins')
        self.losses = data.get('losses')
        self.draws = data.get('draws')

        self.rating = base_rating

        self.ops = set()
        self.hist = list() # Timeline of fighter history
        self.record =  [self.wins,
                        self.losses,
                        self.draws]


class Fight:
    def __init__(self, data):
        self.blue_corner = data.get('blue_corner')# Fighter object
        self.red_corner = data.get('red_corner')

        self.winner = data.get('winner')
        self.loser = self.blue_corner if self.winner==self.blue_corner else self.red_corner if self.winner==self.red_corner else None #data.get('loser','')

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
    def __init__(self):
        self.fighters = dict() #{fighter for fight in self.fights for fighter in fight} #set()
        self.fights = list() 
        # self.v = {fighter.name for fighter in self.fighters} # Vertices (fighters)
        # self.e = set() # Edges (fights)

        self.build()
        self.calculate_ranks()
        self.show_ranks()


    def build(self):
        """
        Loads the data that has been scraped and will fill the FighterGraph
        """
        file_path = 'Fights.json'

        with open(file_path, 'r') as file:
            data = json.load(file)

            for item in data:
                # Check if item is a Fighter
                if "name" in item:
                    print(item)
                    url = item.get('url')
                    if url and url not in self.fighters:
                        self.fighters[url] = Fighter(item)

                # Check if item is a Fight
                elif "blue_corner" in item and "red_corner" in item and "winner" in item:
                    self.fights.append(Fight(item))

        print(" Loaded Fights and Fighters data... ")


    def calculate_ranks(self):
        """
        Calculates ranks for all fights that are available
        """

        for fight in self.fights:
            winner = self.fighters.get(fight.winner)
            loser = self.fighters.get(fight.loser)

            self.update_ratings(winner, loser
                ) if winner and loser else print(f"Skipping fight due to incomplete data: {fight}")  # Check if winner and loser are not None

        print(f" Calculated ranks {len(self.fights)}")   


    @staticmethod
    def update_ratings(winner, loser, K=32):  
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
        exp_winner = 1 / (1 + 10**((loser.rating - winner.rating) / 400)) # Predict outcome of game #rating = op_rating * damp*(w-l) / games
        exp_loser = 1 / (1 + 10**((winner.rating - loser.rating) / 400))
        
        # Actual scores
        score_winner, score_loser = 1,0 
        
        # Update ratings
        winner.rating = winner.rating + K*(score_winner - exp_winner)
        loser.rating = loser.rating + K*(score_loser - exp_loser)

    
    def show_ranks(self):
        # Sort fighter ranks from highest to lowest and print fighter.name: fighter.rank format
        sorted_fighters = sorted(self.fighters.values(), key=lambda fighter: fighter.rating, reverse=True)

        for fighter in sorted_fighters:
            print(f"{fighter.name}: {fighter.rating}")


    def update_ranks(self, new_fights):
        # Updates already calculated ranks with new fighters adding to the data
        pass
        

def main():
    graph = FighterGraph()


main()