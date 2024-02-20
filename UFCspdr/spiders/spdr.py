# https://www.ufcespanol.com/athlete/raoni-haruserosu
import scrapy as s

class ufcSpdr(s.Spider):
    name = "ufc"
    base_url = "https://www.ufcespanol.com"
    allowed_domains = [base_url]

    start_urls = [base_url+"events"]
    fighters = [base_url+"athlete/raoni-haruserosu"]
    event = [base_url+"event/ufc-299"]
    count = 0

    def parse(self, response):
        # Starts crawl
        url = response.url

        if url in self.fighter:
            self.logger.info(f"Updated {url}")
            return
        else:
            self.fighter.add(url)
            count += 1
        
        yield {
            "name": name,

            "wins": wins,
            "losses": losses,
            "draws": draws,

            "strikes": strikes,
            "strikes_landed": strikes_landed,

            "takedowns": takedowns,
            "takedowns_landed": takedowns_landed,

            "win_method": method,

            
        }


    def parseFighter():
        # From the parsed history of upcoming fights, check each of the two fighters fighting career
        pass

    def checkHistory():
        # Checks the start UFC url for upcoming fights
        pass

