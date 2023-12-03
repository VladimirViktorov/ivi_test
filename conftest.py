import pytest
import allure
from api.characters_api import CharactersClient
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
def class_characters_unauthenticated_client(request) -> CharactersClient:
    client = get_http_client(URL.MAIN, None, None)
    return CharactersClient(client=client)