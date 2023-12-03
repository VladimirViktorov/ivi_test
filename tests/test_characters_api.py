import pytest
import allure
from assertions.base.solutions import assert_status_code, assert_error
from assertions.schema import validate_schema
from api.characters_api import CharactersClient
from models.schemes import SCHEMES
from constant import URL, APIErrors

@allure.feature('Characters')
@allure.story('Characters API')
class TestCharacters:
    
    @allure.title("TC-001")
    @allure.description("Correct receipt of all characters")
    def test_get_all_characters(self, class_characters_client: CharactersClient):
        response = class_characters_client.get_characters_api()
        json_response = response.json()
        
        assert_status_code(response.status_code, 200)
        validate_schema(json_response, SCHEMES.CharactersDict)
    
    @allure.title("TC-002")
    @allure.description("Call the method without authentication")
    def test_get_all_characters_with_unauthenticated_client(self, class_characters_unauthenticated_client: CharactersClient):
        response = class_characters_unauthenticated_client.get_characters_api()
        
        assert_status_code(response.status_code, 401)
        assert_error(response.json().get('error', {}), APIErrors.INVALID_AUTHENTICATION)