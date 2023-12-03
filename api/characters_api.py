import allure
from clients.http.client import APIClient
from constant import APIRoutes
from requests import Response

class CharactersClient(APIClient):
    
    @allure.step(f"Getting all characters")
    def get_characters_api(self) -> Response:
        return self.client.get(APIRoutes.CHARACTERS)