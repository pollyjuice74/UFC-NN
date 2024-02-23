# https://www.ufcespanol.com/athlete/raoni-haruserosu
# scrapy shell 'https://www.ufcespanol.com/athlete/raoni-barcelos'
# For using xpath https://doc.scrapy.org/en/latest/topics/selectors.html

import scrapy as s
import re
import sys
import os
from collections import defaultdict

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from UFCspdr.items import FightItem, FighterItem
#from UFC.rank import Fight, Fighter


class ufcSpdr(s.Spider):
    name = "ufc"
    base_url = "https://www.ufcespanol.com"
    allowed_domains = ["www.ufcespanol.com"]

    start_urls = [base_url+"/events"]
    # fights = list() # List of fight objects
    fighters = set() #[base_url+"/athlete/athlete-name"]

    def __init__(self, *args, **kwargs):
        super(ufcSpdr, self).__init__(*args, **kwargs)
        self.events = [self.base_url + "/event/ufc-" + str(i) for i in range(1, 300)]


    def parse(self, response):
        """
        Checks and stores all events' histories
        """
        for event in self.events:
            yield s.Request(event, callback=self.parseEvent)
            

    def parseEvent(self, response):
        """
        Assumes "https://www.ufcespanol.com/event/ufc-i", i in {1,...,299}

        Makes a list of event containing 12 fights. 
            winners: List containing 12 tuples of a fight's fighters and outcome
                    [(blue_url, red_url, outcome), (...), (...), ...]

        That contains data to create a FighterGraph, yields the data and calls further parsing on the fighters.
        """

        ### Data for FighterGraph (v, u, outcome)
        ##########################################################
        # Get blue and red corners
        fighters_blue = response.xpath("//div[@class='c-listing-fight__corner--blue']").getall()
        fighters_red = response.xpath("//div[@class='c-listing-fight__corner--red']").getall()

        winners = self.get_fighters_winner(fighters_blue, fighters_red)
        ##########################################################

        # Parse fighters 
        for blue_url, red_url, outcome in winners:
            # Collect data
            yield FightItem(blue_corner=blue_url, 
                            red_corner=red_url, 
                            winner=outcome)

            # Further parse fighters
            if blue_url:
                yield s.Request(blue_url, callback=self.parseFighter)
            if red_url:
                yield s.Request(red_url, callback=self.parseFighter)


    def get_fighters_winner(self, fighters_blue, fighters_red):
        """
        Input
            fighters_blue: List of 12 blue corner matches with fighter's url and outcome
            fighters_red: List of 12 red corner matches with fighter's url and outcome

            The ith fights of each of these lists correspond to eachother. 

        Output
            blue_url: Url of blue fighter
            red_url: Url of red fighter
            outcome: Url of winner (red or blue) if draw or not fought yet, None

            Returns
            winners: List containing 12 tuples of a fight's fighters and outcome
                [(blue_url, red_url, outcome), (...), (...), ...]
        """
        url_pattern = r'href="(https://www.ufcespanol.com/athlete/[^"]+)"'
        outcome_pattern = r'c-listing-fight__outcome--(win|loss)">\s*(Win|Loss)\s*<'
        
        winners = list()

        for blue_html, red_html in zip(fighters_blue, fighters_red):
            # Extract URLs
            blue_url_search = re.search(url_pattern, blue_html)
            red_url_search = re.search(url_pattern, red_html)
            blue_url = blue_url_search.group(1) if blue_url_search else None
            red_url = red_url_search.group(1) if red_url_search else None

            # Extract outcomes
            blue_outcome_search = re.search(outcome_pattern, blue_html, re.IGNORECASE)
            red_outcome_search = re.search(outcome_pattern, red_html, re.IGNORECASE)
            blue_outcome = 'win' if blue_outcome_search and 'win' in blue_outcome_search.group(1).lower() else None
            red_outcome = 'win' if red_outcome_search and 'win' in red_outcome_search.group(1).lower() else None

            # Determine the winner's URL
            outcome = blue_url if blue_outcome=='win' else red_url if red_outcome=='win' else None
            winners.append((blue_url, red_url, outcome))

        return winners
        # # Date (m,d,y)
        # date_pattern = r"(\w+), (\w+) (\d+) / (\d+:\d+ [AP]M) (-\d+) /"
        # dates = re.findall(date_pattern, text)
        # # add year
            
        # # Assuming https://www.ufcespanol.com/events
        # text = ''.join(response.xpath("//a/text()").getall())


        # # Fighters (F_1, F_2)
        # fighter_pattern = r"([A-Za-z' ]+) vs ([A-Za-z' ]+)"
        # fighters = re.findall(fighter_pattern, text) ###

        # # Links of fighters
        # link_pattern = r"/athlete/([a-z\-]+)"
        # links = re.findall(link_pattern, text)
        # links = [self.base_url + link for link in links]
        # # correct fighter names


    def parseFighter(self, response):
        # Assumes "https://www.ufcespanol.com/athlete/athlete-name"
        # Starts crawl

        if response.url in self.fighters:
            return print(f"Already parsed fighter {response.url}")
        else:
            self.fighters.add(response.url)

        #############################################   
        text = ''.join(response.xpath("//p").getall())  

        # Name
        name = response.xpath("//h1[@class='hero-profile__name']/text()").getall()[0]
        
        # Gets record (W, L, D)
        record_pattern = re.compile(r'(\d+)-(\d+)-(\d+) \(W-L-D\)')
        record = re.findall(record_pattern, text)[0]
        wins, losses, draws = int(record[0]), int(record[1]), int(record[2]) 

        # Opponents
        #opponents = set(response.xpath("//h3/a/@href").getall()) - {response.url}

        yield FighterItem(name=name,
                          url=response.url, 
                          wins=wins, 
                          losses=losses, 
                          draws=draws)

            #"opponents": opponents, # {name: list of w/l/d}
            
            # "strikes": strikes,
            # "strikes_landed": strikes_landed,

            # "takedowns": takedowns,
            # "takedowns_landed": takedowns_landed,

            # "win_method": method,
        #}
        #[Fight(response) for fight in fights]

        # submission_pattern = re.compile(r'Wins by Submission</p>', re.IGNORECASE)
        # method = re.findall(submission_pattern, text)


        # striking_pattern = re.compile(r'<p><strong>Favorite Striking technique: </strong>([^<]+)</p>', re.IGNORECASE)
        # submission_names = defaultdict(int)  # Using defaultdict to automatically handle new submissions
        # striking_techniques = defaultdict(int)  # Similar for striking techniques

        #############################################

        # From the parsed history of upcoming fights, check each of the two fighters fighting career

        # # Check if you ha
        # if fighter_url in self.fighter:
        #     self.logger.info(f"Updated {fighter_url}")
        #     return
        # else:
        #     self.fighter.add(fighter_url)


        # if fighter_url in self.start_urls:
   
        #     for fighter in self.fighters:
        #         yield s.Request(fighter, callback=self.parse)





