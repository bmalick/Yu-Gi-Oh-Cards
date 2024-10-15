import requests
from card import Card

YGO_ENDPOINT = "https://db.ygoprodeck.com/api/v7/cardinfo.php"

class YGODeck:
    def __init__(self, filename, card_name=None, card_type=None, card_atk=None, card_def=None, card_level=None, card_race=None, card_attribute=None, limit=5):
        self.card_name = card_name
        self.card_type = card_type
        self.card_atk = card_atk
        self.card_def = card_def
        self.card_level = card_level
        self.card_race = card_race
        self.card_attribute = card_attribute
        self.limit = limit
        self.filename = filename

    def fetch(self):
        params = {
            "name": self.card_name,
            "type": self.card_type,
            "atk": self.card_atk,
            "def": self.card_def,
            "level": self.card_level,
            "race": self.card_race,
            "attribute": self.card_attribute
            }
        
        response = requests.get(YGO_ENDPOINT, params=params)
        response.raise_for_status()
        cards = response.json()["data"]
        
        count = 0
        
        found_limit = False
        
        for card in cards:
            card_id = card["id"]
            name =  card['name']
            card_type = card["type"]
            description = card["desc"]
            
            attack = card.get("atk")
            defense = card.get("def")
            level = card.get("level")
            archetype = card.get("archetype")
            attribute = card.get("attribute")
            race = card.get("race")
            try:
                rarity = card["card_sets"][0]["set_rarity"]
            except: rarity = None
                
            cardmarket_price = card["card_prices"][0]["cardmarket_price"]
            tcgplayer_price = card["card_prices"][0]["tcgplayer_price"]
            ebay_price = card["card_prices"][0]["ebay_price"]
            amazon_price = card["card_prices"][0]["amazon_price"]
            for i in range(len(card["card_images"])):
                icon = card["card_images"][i]["image_url_small"]
                cover = card["card_images"][i]["image_url"]
                # card_url = card["ygoprodeck_url"]
                
                Card(
                    card_id=card_id,name=name, description=description, card_type=card_type,
                    archetype=archetype, cdm_price=cardmarket_price, tgc_price=tcgplayer_price,
                    ebay_price=ebay_price, amazon_price=amazon_price, attack=attack, defense=defense,
                    level=level, attribute=attribute, race=race, rarity=rarity, icon = icon, cover=cover,
                    # url = card_url, filename = self.filename
                    filename = self.filename
                )
                
                count += 1
                if count>=self.limit:
                    found_limit = True
                    break
            if found_limit:
                break
data = YGODeck(card_name="Sky Striker Ace - Kagari", filename="keys.txt").fetch()

