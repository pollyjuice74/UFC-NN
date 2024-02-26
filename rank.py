# TODO get wins, losses and draws of individual fighters
import os
import json
import uuid


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

        self.fight_ids = set() # Set of fights fought
        self.hist = list() # Timeline of fighter history
        self.record =  [self.wins,
                        self.losses,
                        self.draws]


class Fight:
    def __init__(self, data, fighters):
        self.id = uuid.uuid4()
        self.blue_corner_url = data.get('blue_corner')
        self.red_corner_url = data.get('red_corner')
        self.winner_url = data.get('winner')

        # Convert URLs to Fighter objects
        self.blue_corner = fighters.get(self.blue_corner_url)
        self.red_corner = fighters.get(self.red_corner_url)

        self.winner = fighters.get(self.winner_url) ###
        self.loser = self.blue_corner if self.winner==self.blue_corner else self.red_corner if self.winner==self.red_corner else None #data.get('loser','')

        self.method = None
        self.date = None ###




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
        self.fights = dict() # dict
        # self.v = {fighter.name for fighter in self.fighters} # Vertices (fighters)
        # self.e = set() # Edges (fights)

        self.build()
        self.calculate_ranks()
        self.show_ranks()
        self.save_ranks()


    def build(self):
        file_path = 'Fighters.json'  # Adjusted path for combined data

        with open(file_path, 'r') as file:
            data = json.load(file)
            fight_data = []  # Temporarily store fight data until all fighters are processed

            for item in data:
                if "name" in item:  # Assuming this indicates a fighter entry
                    url = item.get('url')
                    if url and url not in self.fighters:
                        self.fighters[url] = Fighter(item)
                elif "blue_corner" in item and "red_corner" in item and "winner" in item:  # Indicates a fight entry
                    fight_data.append(item)

            # Process fights after all fighters have been instantiated
            for item in fight_data:
                fight = self.create_fight(item)
                if fight: 
                    f_id = fight.id
                    blue_url, red_url = fight.blue_corner_url, fight.red_corner_url

                    # Get objects
                    blue_fighter = self.fighters[blue_url]
                    red_fighter = self.fighters[red_url]

                    # Add fight id to eachothers opponents sets
                    blue_fighter.fight_ids.add(f_id)
                    red_fighter.fight_ids.add(f_id)
                    # Add fight to fights dict
                    self.fights[f_id] = fight

        # Sort fights by date
        #self.fights = sorted(self.fights, key=lambda fight: fight.date)


    def create_fight(self, data):
        # Create and return a Fight object if both fighters are known
        blue_corner = self.fighters.get(data.get('blue_corner'))
        red_corner = self.fighters.get(data.get('red_corner'))
        winner_url = data.get('winner')

        if blue_corner and red_corner:
            fight = Fight(data, self.fighters)  # Assuming Fight's __init__ can handle raw data appropriately
            fight.blue_corner = blue_corner
            fight.red_corner = red_corner
            fight.winner = self.fighters.get(winner_url)

            # Correctly determine the loser
            if fight.winner and fight.winner == blue_corner:
                fight.loser = red_corner
            elif fight.winner and fight.winner == red_corner:
                fight.loser = blue_corner
            else:
                # Handle draw or no contest if applicable
                fight.loser = None

            return fight
        return None


    def calculate_ranks(self):
        """
        Calculates ranks for all fights that are available
        """
        print(f"Starting rank calculations for {len(self.fights)} fights.")
        for fight in self.fights.values():
            # Ensure that both winner and loser are valid Fighter objects
            if fight.winner and fight.loser:
                self.update_ratings(fight.winner, fight.loser)
            else:
                print(f"Skipping fight due to incomplete data or draw. Winner: {fight.winner}, Loser: {fight.loser}")

        print(f"Rank calculations completed.")


    @staticmethod
    def update_ratings(winner, loser, K=32):  
        """
        Input
            winner: Fighter object
            loser: Fighter object
            K: damping factor
        Output
            None
        """  
        # Calculate expected scores
        exp_winner = 1 / (1 + 10**((int(loser.rating) - int(winner.rating)) / 400)) # Predict outcome of game #rating = op_rating * damp*(w-l) / games
        exp_loser = 1 / (1 + 10**((int(winner.rating) - int(loser.rating)) / 400))
        
        # Actual scores
        score_winner, score_loser = 1,0 
        
        # Update ratings
        winner.rating = int(int(winner.rating) + K*(score_winner - float(exp_winner)))
        loser.rating = int(int(loser.rating) + K*(score_loser - float(exp_loser)))

    
    def show_ranks(self):
        #print([fighter.rating for fighter in self.fighters])
        # Sort fighter ranks from highest to lowest and print fighter.name: fighter.rank format
        sorted_fighters = sorted(self.fighters.values(), key=lambda fighter: fighter.rating, reverse=False)

        for fighter in sorted_fighters:
            print(f"{fighter.name}: {fighter.rating}")

    
    def save_ranks(self):
        # Saves fighter ranks to a file
        pass


    def update_ranks(self, new_fights):
        # Updates already calculated ranks with new fighters adding to the data
        pass


    def print(self):
        # for fight in self.fights:
        #     print(fight.blue_corner.name + " vs " + fight.red_corner.name)
        print("Fighters count: ", len(self.fighters))
        print("Fights count: ", len(self.fights))
        


class SampleGraph:
    """
    This is a sample of the FighterGraph that will be used to train the model. 
    """
    def __init__(self, fight, fgraph):
        self.fighters = dict()
        self.fights = set()

        self.build(fight, fgraph)
        #self.prune_graph()
        self.print()
        

    def build(self, fight, fgraph):
        # Get fighter neighbors to a depth of 1
        blue_url, red_url = fight.blue_corner_url, fight.red_corner_url        
        
        red_fighter = fgraph.fighters[red_url]
        blue_fighter = fgraph.fighters[blue_url]
        fighters_set = set() # Temporar set

        for fighter in [red_fighter, blue_fighter]:
            for f_id in fighter.fight_ids:
                opp_url = self.get_opponent(fighter.url, f_id, fgraph)
                if opp_url:
                    opp = fgraph.fighters[opp_url]

                    # Add data to graph
                    for id in opp.fight_ids:
                        self.fights.add(fgraph.fights[id])
                    fighters_set.add(opp_url)
        
        # Make self.fighters dict
        for url in fighters_set: 
            self.fighters[url] = fgraph.fighters[url] 

        
    def get_opponent(self, f_url, fight_id, fgraph):
        # Gets opponent url 
        fight = fgraph.fights[fight_id]
        opp_url = fight.red_corner_url if fight.blue_corner_url==f_url else fight.blue_corner_url if fight.red_corner_url==f_url else None
        return opp_url


    def prune_graph(graph, date):
        # Removes all nodes from the graph where the fight's date is after 'date' 
        sample_graph = graph.deepcopy()

        for fight in graph.fights: # Make it so it starts at the latest fight for efficiency
            if fight.date > date:
                sample_graph.remove(fight)
            else:
                break

    def print(self):
        # for fight in self.fights:
        #     print(fight.blue_corner.name + " vs " + fight.red_corner.name)
        print("Fighters count: ", len(self.fighters))
        print("Fights count: ", len(self.fights))


def main():
    fgraph = FighterGraph()
    k = list(fgraph.fights.keys())[0]
    fight = fgraph.fights[k]
    print(fight.blue_corner_url, fight.red_corner_url)

    sgraph = SampleGraph(fight, fgraph)
    fgraph.print()

main()