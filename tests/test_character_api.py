import pytest
import allure
from assertions.base.solutions import assert_status_code, assert_error, assert_len_database, assert_error_data
from assertions.schema import validate_schema, validate_data, check_change_data
from api.character_api import CharacterClient
from api.characters_api import CharactersClient
from models.schemes import SCHEMES
from constant import URL, APIErrors

@allure.feature('Character')
@allure.story('Character API')
class TestCharacter:
    
    @allure.title("TC-003")
    @allure.description("Correctly obtaining information about a character")
    @pytest.mark.parametrize('name', ['3-D Man',
                                      'Agent Brand',
                                      'Ancient One (Ultimate)',
                                      'Anole'])
    def test_get_info_about_character(self, class_character_client: CharacterClient, name: str):
        response = class_character_client.get_character_api(name)
        json_response = response.json()
        
        assert_status_code(response.status_code, 200)
        validate_schema(json_response, SCHEMES.CharacterDict)
    
    @allure.title("TC-004")
    @allure.description("Call the method without authentication")
    @pytest.mark.parametrize('name', ['3-D Man'])
    def test_get_ainfo_about_character_with_unauthenticated_client(self, class_character_unauthenticated_client: CharacterClient, name: str):
        response = class_character_unauthenticated_client.get_character_api(name)
        
        assert_status_code(response.status_code, 401)
        assert_error(response.json().get('error', {}), APIErrors.INVALID_AUTHENTICATION)
    
    @allure.title("TC-005")
    @allure.description("Finding a character with a nonexistent name")
    @pytest.mark.parametrize('name', ['Test'])
    def test_get_info_about_character_nonexistent(self, class_character_client: CharacterClient, name: str):
        response = class_character_client.get_character_api(name)
        
        assert_status_code(response.status_code, 400)
        assert_error(response.json().get('error', {}), APIErrors.NO_SUCH_NAME)
        
    @allure.title("TC-006")
    @allure.description("Create a new character")
    @pytest.mark.parametrize('body', [{"name": "Hawkeye",
                                       "universe": "Marvel Universe",
                                       "education": "High school (unfinished)",
                                       "weight": 104,
                                       "height": 1.90,
                                       "identity": "Publicly known"
                                       },
                                      {"name": "test"},
                                      {"name": "Hulk",
                                       "universe": "Marvel Universe",
                                       "education": "High school (unfinished)",
                                       "other_aliases": "Marvel Man, Starknight",
                                       "weight": 104,
                                       "height": 1.90,
                                       "identity": "Publicly known"
                                       }])
    def test_post_new_character(self, class_character_client: CharacterClient, reset_database, body: dict):
        response = class_character_client.post_character_api(body)
        json_response = response.json()
        
        assert_status_code(response.status_code, 200)
        validate_schema(json_response, SCHEMES.CharacterDict)
    
    @allure.title("TC-007")
    @allure.description("Attempting to add a character when the database is full")
    def test_full_database(self, class_character_client: CharacterClient, class_characters_client: CharactersClient, reset_database):
        for i in range(500):
            response = class_character_client.post_character_api({"name": f"test{i}"})
            if response.status_code != 200:
                break
        response_characters = class_characters_client.get_characters_api()
        assert_len_database(len(response_characters.json().get('result', {})), 500)
        response = class_character_client.post_character_api({"name": f"test999"})
        assert_status_code(response.status_code, 400)
        assert_error(response.json().get('error', {}), APIErrors.COLLECTION_500_ITEMS)
        
    @allure.title("TC-008")
    @allure.description("Create a new character without name")
    @pytest.mark.parametrize('body', [{"universe": "Marvel Universe",
                                       "education": "High school (unfinished)",
                                       "other_aliases": "Marvel Man, Starknight",
                                       "weight": 104,
                                       "height": 1.90,
                                       "identity": "Publicly known"
                                       }])
    def test_post_new_character_without_name(self, class_character_client: CharacterClient, reset_database, body: dict):
        response = class_character_client.post_character_api(body)
        
        assert_status_code(response.status_code, 400)
        assert_error(response.json().get('error', {}), APIErrors.MISSING_NAME)
    
    @allure.title("TC-009")
    @allure.description("Create a new character with invalid data")
    @pytest.mark.parametrize('body', [{"name": "Hulk",
                                       "universe": 55,
                                       "education": "High school (unfinished)",
                                       "other_aliases": "Marvel Man, Starknight",
                                       "weight": "df",
                                       "height": 1.90,
                                       "identity": "Publicly known"
                                       },
                                      {"name": "Hulk",
                                       "universe": "test",
                                       "education": "High school (unfinished)",
                                       "other_aliases": 5,
                                       "weight": 12,
                                       "height": "test",
                                       "identity": "Publicly known"
                                       }])
    def test_post_new_character_with_invalid_data(self, class_character_client: CharacterClient, reset_database, body: dict):
        response = class_character_client.post_character_api(body)
        
        invalid_list = validate_data(SCHEMES.CharacterDict, {"result" :body})
        assert_status_code(response.status_code, 400)
        for invalid_field in invalid_list:
            assert_error_data(response.json().get('error', {}), APIErrors.INVALID_DATA[invalid_field])
    
    @allure.title("TC-010")
    @allure.description("Create a new character with null data")
    @pytest.mark.parametrize('body', [{"name": None,
                                       "universe": None,
                                       "education": None,
                                       "other_aliases": None,
                                       "weight": None,
                                       "height": None,
                                       "identity": None
                                       },
                                      {"name": "Hulk",
                                       "universe": "test",
                                       "education": "High school (unfinished)",
                                       "other_aliases": None,
                                       "weight": 12,
                                       "height": None,
                                       "identity": "Publicly known"
                                       }])
    def test_post_new_character_with_null_data(self, class_character_client: CharacterClient, reset_database, body: dict):
        response = class_character_client.post_character_api(body)
        
        assert_status_code(response.status_code, 400)
        for invalid_field in body:
            if invalid_field == None:
                assert_error_data(response.json().get('error', {}), APIErrors.NULL_DATA[invalid_field])
    
    @allure.title("TC-011")
    @allure.description("Create a new character with invalid schema")
    @pytest.mark.parametrize('body', ["test",
                                      123,
                                      ["a", "b", "c"]])
    def test_post_new_character_with_invalid_schema(self, class_character_client: CharacterClient, reset_database, body: dict):
        response = class_character_client.post_character_api(body)
        
        assert_status_code(response.status_code, 400)
        assert_error(response.json().get('error', {}), APIErrors.INVALID_SCHEMA)
    
    @allure.title("TC-012")
    @allure.description("Create a new character with extra data")
    @pytest.mark.parametrize('body', [{"name": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaafaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                                       "universe": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaafaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                                       "education": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaafaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                                       "other_aliases": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaafaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                                       "weight": 1000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000003,
                                       "height": -1000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000003,
                                       "identity": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaafaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
                                       },
                                      {"name": "Hulk",
                                       "universe": "test",
                                       "education": "High school (unfinished)",
                                       "other_aliases": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaafaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                                       "weight": 12,
                                       "height": 1000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000003,
                                       "identity": "Publicly known"
                                       }])
    def test_post_new_character_with_extra_data(self, class_character_client: CharacterClient, reset_database, body: dict):
        response = class_character_client.post_character_api(body)
        
        assert_status_code(response.status_code, 400)
        for invalid_field in body:
            if invalid_field == None:
                assert_error_data(response.json().get('error', {}), APIErrors.EXTRA_DATA[invalid_field])
    
    @allure.title("TC-013")
    @pytest.mark.need_review
    @allure.description("Create a character that is available in the base")
    @pytest.mark.parametrize('body', [{"name": "Hawkeye",
                                       "universe": "Marvel Universe",
                                       "education": "High school (unfinished)",
                                       "weight": 104,
                                       "height": 1.90,
                                       "identity": "Publicly known"
                                       },
                                      {"name": "test"},
                                      {"name": "Hulk",
                                       "universe": "Marvel Universe",
                                       "education": "High school (unfinished)",
                                       "other_aliases": "Marvel Man, Starknight",
                                       "weight": 104,
                                       "height": 1.90,
                                       "identity": "Publicly known"
                                       }])
    def test_post_new_character_is_available_in_base(self, class_character_client: CharacterClient, reset_database, body: dict):
        response = class_character_client.post_character_api(body)
        response = class_character_client.post_character_api(body)
        
        assert_status_code(response.status_code, 400)
        assert_error(response.json().get('error', {}), APIErrors.ALREADY_EXISTS.substitute(name=body["name"]))
    
    @allure.title("TC-014")
    @allure.description("Change the character")
    @pytest.mark.parametrize('body', [{"name": "Ajak",
                                       "universe": "Marvel Universe",
                                       "education": "High school (unfinished)",
                                       "other_aliases": "Marvel Man, Starknight",
                                       "weight": 104,
                                       "height": 1.90,
                                       "identity": "Publicly known"
                                       },
                                      {"name": "Amanda Sefton",
                                       "identity": "Test"
                                       }])
    def test_put_change_character(self, class_character_client: CharacterClient, reset_database, body: dict):
        original_data_response = class_character_client.get_character_api(body["name"])
        original_data = original_data_response.json().get('result', {})
        response = class_character_client.put_character_api(body)
        updated_data_response = class_character_client.get_character_api(body["name"])
        updated_data = updated_data_response.json().get('result', {})
        json_response = response.json()
        
        assert_status_code(response.status_code, 200)
        validate_schema(json_response, SCHEMES.CharacterDict)
        check_change_data(original_data, updated_data, body)
        
    @allure.title("TC-015")
    @allure.description("Change the character without name")
    @pytest.mark.parametrize('body', [{"universe": "Marvel Universe",
                                       "education": "High school (unfinished)",
                                       "other_aliases": "Marvel Man, Starknight",
                                       "weight": 104,
                                       "height": 1.90,
                                       "identity": "Publicly known"
                                       }])
    def test_put_character_without_name(self, class_character_client: CharacterClient, reset_database, body: dict):
        response = class_character_client.put_character_api(body)
        
        assert_status_code(response.status_code, 400)
        assert_error(response.json().get('error', {}), APIErrors.MISSING_NAME)
    
    @allure.title("TC-016")
    @allure.description("Change the character with invalid data")
    @pytest.mark.parametrize('body', [{"name": "Ajak",
                                       "universe": 0,
                                       "education": 0,
                                       "other_aliases": 0,
                                       "weight": "test",
                                       "height": "test",
                                       "identity": 0
                                       },
                                      {"name": "Ajak",
                                       "universe": "Marvel Universe",
                                       "education": "High school (unfinished)",
                                       "other_aliases": "Marvel Man, Starknight",
                                       "weight": 104,
                                       "height": "test",
                                       "identity": 0
                                       }])
    def test_put_character_with_invalid_data(self, class_character_client: CharacterClient, reset_database, body: dict):
        response = class_character_client.put_character_api(body)
        
        invalid_list = validate_data(SCHEMES.CharacterDict, {"result" :body})
        assert_status_code(response.status_code, 400)
        for invalid_field in invalid_list:
            assert_error_data(response.json().get('error', {}), APIErrors.INVALID_DATA[invalid_field])
    
    @allure.title("TC-017")
    @allure.description("Change the character with null data")
    @pytest.mark.parametrize('body', [{"name": "Ajak",
                                       "universe": None,
                                       "education": None,
                                       "other_aliases": None,
                                       "weight": None,
                                       "height": None,
                                       "identity": None
                                       },
                                      {"name": "Hulk",
                                       "universe": "test",
                                       "education": "High school (unfinished)",
                                       "other_aliases": None,
                                       "weight": 12,
                                       "height": None,
                                       "identity": "Publicly known"
                                       }])
    def test_put_character_with_null_data(self, class_character_client: CharacterClient, reset_database, body: dict):
        response = class_character_client.put_character_api(body)
        
        assert_status_code(response.status_code, 400)
        for invalid_field in body:
            if invalid_field == None:
                assert_error_data(response.json().get('error', {}), APIErrors.NULL_DATA[invalid_field])
    
    @allure.title("TC-018")
    @allure.description("Change the character with invalid schema")
    @pytest.mark.parametrize('body', ["test",
                                      123,
                                      ["a", "b", "c"]])
    def test_put_character_with_invalid_schema(self, class_character_client: CharacterClient, reset_database, body: dict):
        response = class_character_client.put_character_api(body)
        
        assert_status_code(response.status_code, 400)
        assert_error(response.json().get('error', {}), APIErrors.INVALID_SCHEMA)
    
    @allure.title("TC-019")
    @allure.description("Change the character with extra data")
    @pytest.mark.parametrize('body', [{"name": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaafaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                                       "universe": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaafaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                                       "education": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaafaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                                       "other_aliases": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaafaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                                       "weight": 1000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000003,
                                       "height": -1000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000003,
                                       "identity": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaafaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
                                       },
                                      {"name": "Hulk",
                                       "universe": "test",
                                       "education": "High school (unfinished)",
                                       "other_aliases": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaafaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                                       "weight": 12,
                                       "height": 1000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000003,
                                       "identity": "Publicly known"
                                       }])
    def test_put_character_with_extra_data(self, class_character_client: CharacterClient, reset_database, body: dict):
        response = class_character_client.put_character_api(body)
        
        assert_status_code(response.status_code, 400)
        for invalid_field in body:
            if invalid_field == None:
                assert_error_data(response.json().get('error', {}), APIErrors.EXTRA_DATA[invalid_field])
    