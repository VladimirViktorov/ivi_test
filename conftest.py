import pytest
import allure
from api.characters_api import CharactersClient
from api.character_api import CharacterClient
from api.reset_api import ResetClient
from clients.http.builder import get_http_client
from constant import URL

def pytest_addoption(parser):
    """
    Добавляет параметры командной строки для pytest.
    :param parser: Парсер для аргументов командной строки.
    """
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
    """
    Фикстура pytest для создания экземпляра класса CharactersClient с аутентификацией.
    :param request: Объект запроса фикстуры.
    :return: Экземпляр класса CharactersClient.
    """
    login = request.config.getoption("--login")
    password = request.config.getoption("--password")
    client = get_http_client(URL.MAIN, login, password)
    return CharactersClient(client=client)

@pytest.fixture(scope="class")
def class_characters_unauthenticated_client() -> CharactersClient:
    """
    Фикстура pytest для создания экземпляра класса CharactersClient без аутентификации.
    :return: Экземпляр класса CharactersClient.
    """
    client = get_http_client(URL.MAIN, None, None)
    return CharactersClient(client=client)

@pytest.fixture(scope="class")
def class_character_client(request) -> CharacterClient:
    """
    Фикстура pytest для создания экземпляра класса CharacterClient с аутентификацией.
    :param request: Объект запроса фикстуры.
    :return: Экземпляр класса CharacterClient.
    """
    login = request.config.getoption("--login")
    password = request.config.getoption("--password")
    client = get_http_client(URL.MAIN, login, password)
    return CharacterClient(client=client)

@pytest.fixture(scope="class")
def class_character_unauthenticated_client() -> CharacterClient:
    """
    Фикстура pytest для создания экземпляра класса CharacterClient без аутентификации.
    :return: Экземпляр класса CharacterClient.
    """
    client = get_http_client(URL.MAIN, None, None)
    return CharacterClient(client=client)

@pytest.fixture(scope="session")
def class_reset_client(request) -> ResetClient:
    """
    Фикстура pytest для создания экземпляра класса ResetClient с аутентификацией.
    Используется для сброса состояния базы данных между тестовыми сессиями.
    :param request: Объект запроса фикстуры.
    :return: Экземпляр класса ResetClient.
    """
    login = request.config.getoption("--login")
    password = request.config.getoption("--password")
    client = get_http_client(URL.MAIN, login, password)
    return ResetClient(client=client)

@pytest.fixture(scope="function")
def reset_database(class_reset_client):
    """
    Фикстура pytest для сброса состояния базы данных после выполнения теста.
    :param class_reset_client: Фикстура класса ResetClient для вызова метода сброса.
    """
    yield

    with allure.step("Reset data"):
        class_reset_client.post_reset_api()