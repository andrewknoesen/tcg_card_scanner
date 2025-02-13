import requests


class SWUDB:
    def __init__(self):
        self.base_url = "https://api.swu-db.com"

    def search_card(self, card_name: str):
        q = {"q": card_name, "format": "json", "pretty": True}
        r = requests.get(f"{self.base_url}/cards/search", params=q, timeout=500)
        return r.json()

    def get_card(self, set: str, number: int):
        q = {"format": "json", "pretty": True}
        r = requests.get(f"{self.base_url}/cards/{set}/{number}", params=q, timeout=500)
        print(r.url)
        return r.json()
