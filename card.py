import requests



class Card:
    notion_api = "https://api.notion.com/v1/"
    
    def __init__(self, card_id, name, description, card_type, race, archetype, rarity, cdm_price, tgc_price, ebay_price, amazon_price, attack, defense, level, attribute, icon, cover, filename):
        self.card_id = card_id
        self.name = name
        self.description = description
        self.card_type = card_type
        self.race = race
        self.archetype = archetype
        self.rarity = rarity
        self.cdm_price = cdm_price
        self.ebay_price = ebay_price
        self.tgc_price = tgc_price
        self.amazon_price = amazon_price
        self.attack = attack
        self.defense = defense
        self.level = level
        self.attribute = attribute
        self.icon = icon
        self.cover = cover
        self.star = "⭐"
        self.filename = filename
        # self.url = url
        
        self.get_params()
        self.add_to_db()
    
    def get_params(self):
        with open(self.filename,"r") as file:
            content = file.read()

        token, self.db_id = content.split("\n")[:2]
        self.db_id = self.db_id.split("?")[0].split("/")[-1]
            


        self.headers = {
            "Authorization": "Bearer " + token,
            "accept": "application/json",
            "Notion-Version": "2022-06-28",
            "content-type": "application/json"
        }

    
    def __str__(self) -> str:
        return "Name: {}\nType: {}\nDescription: {}\n".format(self.name, self.card_type, self.description)

    def replace_none_int(self, var): return var if var is not None else 0

    def replace_none_str(self, var): return var if var is not None else ''

    def add_to_db(self):
        self.attack = self.replace_none_int(self.attack)
        self.defense = self.replace_none_int(self.defense)
        self.level = self.replace_none_int(self.level)
        self.attribute = self.replace_none_str(self.attribute)
        self.race = self.replace_none_str(self.race)
        self.description = self.replace_none_str(self.description)
        self.archetype = self.replace_none_str(self.archetype)
        self.card_type = self.replace_none_str(self.card_type)
        self.rarity = self.replace_none_str(self.rarity)
        # self.url = self.replace_none_str(self.url)
        self.cdm_price = self.replace_none_int(self.cdm_price)
        self.tgc_price = self.replace_none_int(self.tgc_price)
        self.ebay_price = self.replace_none_int(self.ebay_price)
        self.amazon_price = self.replace_none_int(self.amazon_price)

        payload = {
            "parent":{
                "type": "database_id",
                "database_id": self.db_id
            },
            
            "icon": {
                "type": "external",
                "external": {"url": self.icon}
            },
            
            "cover": {
                "type": "external",
                "external": {"url": self.cover}
            },
            
            "properties": {
                "Id": {"number": self.card_id},
                "Name": {"title":[{"text": {"content": self.name}}]},
                "Attack": {"number": self.attack},
                "Defense": {"number": self.defense},
                "Level": {"number": self.level},
                "Attribute": {"select": {"name": self.attribute}},
                "Stars": {"rich_text":[{"text": {"content": self.level*self.star}}]},
                "Race": {"select": {"name": self.race}},
                "Archetype": {"rich_text": [{"text": {"content": self.archetype}}]},
                "Type": {"select": {"name": self.card_type}},
                "Rarity": {"select": {"name": self.rarity}},
                "Card Market Price": {"number": float(self.cdm_price)},
                "TGC Player Price": {"number": float(self.tgc_price)},
                "eBay Price": {"number": float(self.ebay_price)},
                "Amazon Price": {"number": float(self.amazon_price)},     
                # "Url": {"url": self.url}
            },
            
            "children": [
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {"rich_text": [{"text": {"content": self.description}}]}
                }
            ]
        }
        
        response = requests.post(self.notion_api+"pages/", headers=self.headers, json=payload)
        response.raise_for_status()
