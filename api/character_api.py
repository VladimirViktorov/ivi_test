import allure
from clients.http.client import APIClient
from constant import APIRoutes
from requests import Response

class CharacterClient(APIClient):
    
    def get_character_api(self, name_character) -> Response:
        with allure.step(f"Get information about a character named '{name_character}'"):
            params = {'name': name_character}
            return self.client.get(APIRoutes.CHARACTER, params=params)
    
    def post_character_api(self, body: dict) -> Response:
        with allure.step(f"Create a new character with the parameters '{body}'"):
            return self.client.post(APIRoutes.CHARACTER, json=body)
    
    def put_character_api(self, body: dict) -> Response:
        with allure.step(f"Change the character with the parameters '{body}'"):
            return self.client.put(APIRoutes.CHARACTER, json=body)