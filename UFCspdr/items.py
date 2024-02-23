# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class UfcspdrItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class FightItem(scrapy.Item):
    # Example fields for fight data
    blue_corner = scrapy.Field()
    red_corner = scrapy.Field()
    winner = scrapy.Field()

class FighterItem(scrapy.Item):
    # Example fields for fighter data
    name = scrapy.Field()
    url = scrapy.Field()
    wins = scrapy.Field()
    losses = scrapy.Field()
    draws = scrapy.Field()
    # Add more fields as necessary