# https://www.ufcespanol.com/athlete/raoni-haruserosu
# scrapy shell 'https://www.ufcespanol.com/athlete/raoni-barcelos'
# For using xpath https://doc.scrapy.org/en/latest/topics/selectors.html

import scrapy as s
import re
from collections import defaultdict
from UFC.rank import Fight, Fighter

class ufcSpdr(s.Spider):
    name = "ufc"
    base_url = "https://www.ufcespanol.com"
    allowed_domains = [base_url]

    start_url = [base_url+"/events"]
    fighters = set() #[base_url+"/athlete/raoni-haruserosu"]
    event = set() #[base_url+"/event/ufc-299"]


    def parse(self, response):
        pass
        

    def parseFighter(self, response):
        # Starts crawl
        fighter_url = response.url

        #############################################   
        text = ''.join(response.xpath("//p").getall())  

        # Name
        name = response.xpath("//h1[@class='hero-profile__name']/text()").getall()[0]
        
        # Gets record (W, L, D)
        record_pattern = re.compile(r'(\d+)-(\d+)-(\d+) \(W-L-D\)')
        record = re.findall(record_pattern, text)[0]
        wins, losses, draws = int(record[0]), int(record[1]), int(record[2]) 

        # Opponents
        opponents = set(response.xpath("//h3/a/@href").getall()) - {fighter_url}
        [Fight(response) for fight in fights]
        
        



        # submission_pattern = re.compile(r'Wins by Submission</p>', re.IGNORECASE)
        # method = re.findall(submission_pattern, text)


        # striking_pattern = re.compile(r'<p><strong>Favorite Striking technique: </strong>([^<]+)</p>', re.IGNORECASE)
        # submission_names = defaultdict(int)  # Using defaultdict to automatically handle new submissions
        # striking_techniques = defaultdict(int)  # Similar for striking techniques

        #############################################



        # From the parsed history of upcoming fights, check each of the two fighters fighting career
        yield {
            "name": name,

            "wins": wins,
            "losses": losses,
            "draws": draws,

            "opponents": opponents, # {name: list of w/l/d}
            
            # "strikes": strikes,
            # "strikes_landed": strikes_landed,

            # "takedowns": takedowns,
            # "takedowns_landed": takedowns_landed,

            # "win_method": method,
        }

        # # Check if you ha
        # if fighter_url in self.fighter:
        #     self.logger.info(f"Updated {fighter_url}")
        #     return
        # else:
        #     self.fighter.add(fighter_url)


        # if fighter_url in self.start_urls:
   
        #     for fighter in self.fighters:
        #         yield s.Request(fighter, callback=self.parse)




    def checkHistory(self, response):
        # Assuming https://www.ufcespanol.com/events
        text = ''.join(response.xpath("//a/text()").getall())

        # Date (m,d,y)
        date_pattern = r"(\w+), (\w+) (\d+) / (\d+:\d+ [AP]M) (-\d+) /"
        dates = re.findall(date_pattern, text)
        # add year

        # Fighters (F_1, F_2)
        fighter_pattern = r"([A-Za-z' ]+) vs ([A-Za-z' ]+)"
        fighters = re.findall(fighter_pattern, text) ###

        # Links of fighters
        link_pattern = r"/athlete/([a-z\-]+)"
        links = re.findall(link_pattern, text)
        links = [self.base_url + link for link in links]
        # correct fighter names

