# UFC predictor

Onworking project to get UFC figher and fights data, use Elo Ranking Algorithm on them and then add Neural Network Weights to process the data and make better win/loss predictions.


Tree

## Layout

In `UFCSpdr/spiders/spdr.py` there is a definition for a web crawling spider `ufcSpdr(scrapy.Spider)` that will get information on `Fighters` and `Fights`.

On `rank.py` there is an implementation for three classes:

`FighterGraph` 
  - Graph to calculate Elo Rating for UFC fighters. 
- Formaly defined as G = (E, V), where
        -- E = {(fighter_1, fighter_2) | for fighter_i in fight for fight in all_fights},
        -- V = {fighter | for fighter in fighters_set}
  
  `Fighter`
  `Fight`

---

## Resources

- UFC Events
  https://www.ufcespanol.com/events

- Elo Ranking Algorithm
  https://github.com/markmusic2727/elo_rating_algorithm/blob/master/algorithm/dart/algorithm.dart

- UFC Stats
  http://ufcstats.com/fighter-details/93fe7332d16c6ad9

- UFC Fight Nights
  https://www.ufcespanol.com/event/ufc-fight-night-february-24-2024
