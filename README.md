# Yu-Gi-Oh-Cards
### Automated Notion Template.

Fetch Yu-Gi-Oh Cards from the API [Yu-Gi-Oh API](https://ygoprodeck.com/api-guide/) then update your database using Notion API.

<!-- <img src=".\images\IMG-4304.jpg" alt="Card"> -->


# Notion Database

<img src=".\images\cover1.png" alt="Notion database">

# Installation

Requirements:

* python-dotenv==1.0.0
* requests==2.28.1

Install the required module:

```bash
pip install -r requirements.txt
```

# Run it by your self

**Make sure to provide in the .env file your Notion API key and your database id.**

The file main.py will fetch the Yu-Gi-Oh Cards.
Cards can be fetch by filtering through their (we five their parser arguements):

* name : card_name
* type : card_type
* atk : card_atk
* def : card_def
* level : card_level
* race : card_race
* attribute : card_attribute

You can limit the number of cards retrieved (limit is the parser argument, default value is 10).

Here are some examples of code you can run :

1. Fetch by name:
```bash
python3 main.py --card_name "Dark Magician"
```

2. Fetch by type:
```bash
python3 main.py --card_type "Fusion Monster" --limit 20
```

3. Fetch by attaque points:
```bash
python3 main.py --card_atk 2500 --limit 20
```

4. Fetch by defense points:
```bash
python3 main.py --card_def 2000 --limit 20
```

5. Fetch by level:
```bash
python3 main.py --card_level 8 --limit 20
```

6. Fetch by race:
```bash
python3 main.py --card_race "Warrior" --limit 20
```

