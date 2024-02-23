# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from items import FightItem, FighterItem


class UfcspdrPipeline:
    def process_item(self, item, spider):
        return item

# pipelines.py
class FightPipeline:
    def process_item(self, item, spider):
        if isinstance(item, FightItem):
            # Code to export FightItems to Fights.json
            # This can be as simple as appending to a file
            return item

class FighterPipeline:
    def process_item(self, item, spider):
        if isinstance(item, FighterItem):
            # Code to export FighterItems to Fighters.json
            # This can be appending to another file
            return item
