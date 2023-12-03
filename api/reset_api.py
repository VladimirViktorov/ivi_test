import allure
from clients.http.client import APIClient
from constant import APIRoutes
from requests import Response

class ResetClient(APIClient):
    
    @allure.step(f"Reset data")
    def post_reset_api(self) -> Response:
        return self.client.post(APIRoutes.RESET)