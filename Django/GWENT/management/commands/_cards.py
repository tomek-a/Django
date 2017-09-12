from urllib.request import Request, urlopen
import json
from GWENT.models import Card


def get_cards():
    url = Request(
        'https://api.gwentapi.com/v0/cards?limit=305',  # actual card pool size 305
        headers={"User-Agent": "Magic-Browser"}
    )
    r = urlopen(url)
    data_ = r.read().decode(r.info().get_param('charset') or 'utf-8')
    data = json.loads(str(data_))
    card_list = data['results']

    for card in card_list:
        card_href = card['href']
        url_card = Request(card_href, headers={"User-Agent": "Magic-Browser"})
        r_card = urlopen(url_card)
        card_data_ = r_card.read().decode(r_card.info().get_param('charset') or 'utf-8')
        card_data = json.loads(str(card_data_))
        variation_href = card_data['variations'][0]['href']

        url_variation = Request(variation_href, headers={"User-Agent": "Magic-Browser"})
        r_var = urlopen(url_variation)
        card_variation_ = r_var.read().decode(r_var.info().get_param('charset') or 'utf-8')
        card_variation = json.loads(str(card_variation_))

        try:
            strength = card_data['strength']
        except:
            strength = 'None'

        card = {
            "name": card_data['name'],
            "faction": card_data['faction']['name'],
            "card_set": card_data['variations'][0]['availability'],
            "text": card_data['info'],
            "type": card_data['group']['name'],
            "rarity": card_data['variations'][0]['rarity']['name'],
            "flavor": card_data['flavor'],
            "strength": strength,
            "artist": card_variation['art']['artist'],
            "craft_normal": card_variation['craft']['normal'],
            "craft_premium": card_variation['craft']['premium'],
            "mill_normal": card_variation['mill']['normal'],
            "mill_premium": card_variation['craft']['premium'],
            "thumbnail_link": card_variation['art']['thumbnailImage'],
        }

        Card.objects.create(**card)
