from clients.http.client import HTTPClient

def get_http_client(url: str, username: str, password: str) -> HTTPClient:
    """
    Создает и возвращает экземпляр HTTPClient с заданными параметрами аутентификации.
    :param url: Базовый URL для HTTP-клиента.
    :param username: Имя пользователя для аутентификации.
    :param password: Пароль пользователя для аутентификации.
    :return: Экземпляр HTTPClient.
    """
    return HTTPClient(base_url=url, username=username, password=password)
