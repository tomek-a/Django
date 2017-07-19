from urllib.request import Request, urlopen
import json


class Card:
    def __init__(self):
        url_request = Request(
            'https://api.gwentapi.com/v0/cards?limit=305',  # actuall card pool size 305
            headers={"User-Agent": "Magic-Browser"}
        )
        r = urlopen(url_request)
        data_ = r.read().decode(r.info().get_param('charset') or 'utf-8')
        data = json.loads(str(data_))
        card_list = data['results']
        return card_list

    def getCard(self, card_id):
        card_id = int(card_id) - 1
        card_link = self.card_list[card_id]['href']

        card_url_request = Request(card_link, headers={"User-Agent": "Magic-Browser"})
        r_card = urlopen(card_url_request)
        card_data_ = r_card.read().decode(r_card.info().get_param('charset') or 'utf-8')
        card_data = json.loads(str(card_data_))
        thumbnail_link_json = card_data['variations'][0]['href']

        thumbnail_url_request = Request(thumbnail_link_json, headers={"User-Agent": "Magic-Browser"})
        r_thumb = urlopen(thumbnail_url_request)
        thumb_data_ = r_thumb.read().decode(r_thumb.info().get_param('charset') or 'utf-8')
        thumbnail = json.loads(str(thumb_data_))
        thumbnail_link = thumbnail['art']['thumbnailImage']

        try:
            strength = card_data['strength']
        except:
            strength = 'None'
        ctx = {
            'name': card_data['name'],
            'faction': card_data['faction']['name'],
            'text': card_data['info'],
            'strength': strength,
            'type': card_data['group']['name'],
            'rarity': card_data['variations'][0]['rarity']['name'],
            'row': ', '.join(card_data['positions']),
            'flavor': card_data['flavor'],
            'thumbnail_link': thumbnail_link
        }

        return ctx
