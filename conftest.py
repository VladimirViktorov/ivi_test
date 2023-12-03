import pytest
import allure
from api.characters_api import CharactersClient
from api.character_api import CharacterClient
from api.reset_api import ResetClient
from clients.http.builder import get_http_client
from constant import URL

def pytest_addoption(parser):
    parser.addoption(
        "--login", 
        action="store", 
        default='username', 
        help="Login for authentication"
    )
    parser.addoption(
        "--password", 
        action="store", 
        default='password', 
        help="Password for authentication"
    )

@pytest.fixture(scope="class")
def class_characters_client(request) -> CharactersClient:
    login = request.config.getoption("--login")
    password = request.config.getoption("--password")
    client = get_http_client(URL.MAIN, login, password)
    return CharactersClient(client=client)

@pytest.fixture(scope="class")
def class_characters_unauthenticated_client() -> CharactersClient:
    client = get_http_client(URL.MAIN, None, None)
    return CharactersClient(client=client)

@pytest.fixture(scope="class")
def class_character_client(request) -> CharacterClient:
    login = request.config.getoption("--login")
    password = request.config.getoption("--password")
    client = get_http_client(URL.MAIN, login, password)
    return CharacterClient(client=client)

@pytest.fixture(scope="class")
def class_character_unauthenticated_client() -> CharacterClient:
    client = get_http_client(URL.MAIN, None, None)
    return CharacterClient(client=client)

@pytest.fixture(scope="session")
def class_reset_client(request) -> ResetClient:
    login = request.config.getoption("--login")
    password = request.config.getoption("--password")
    client = get_http_client(URL.MAIN, login, password)
    return ResetClient(client=client)

@pytest.fixture(scope="function")
def reset_database(class_reset_client):
    yield

    with allure.step("Reset data"):
        class_reset_client.post_reset_api()