import typing
import requests
import allure
from requests import Response
from requests.auth import AuthBase
from requests.auth import HTTPBasicAuth
from urllib.parse import urljoin

URLTypes = str
QueryParamTypes = typing.Optional[typing.Dict[str, str]]
HeaderTypes = typing.Optional[typing.Dict[str, str]]
CookieTypes = typing.Optional[typing.Dict[str, str]]
RequestData = typing.Optional[typing.Union[typing.Dict[str, str], typing.List[typing.Tuple[str, str]], str]]
RequestFiles = typing.Optional[typing.Dict[str, typing.Any]]
TimeoutTypes = typing.Optional[typing.Union[float, typing.Tuple[float, float]]]

class HTTPClient:
    def __init__(self, base_url=None, username=None, password=None):
        """
        Инициализация HTTP-клиента с возможностью задать базовый URL, а также данные для аутентификации.
        :param base_url: Базовый URL для запросов.
        :param username: Имя пользователя для аутентификации.
        :param password: Пароль пользователя.
        """
        self.session = requests.Session()
        if base_url:
            self.base_url = base_url
        
        if username and password:
            self.session.auth = HTTPBasicAuth(username, password)
    
    def _full_url(self, path):
        """
        Формирует полный URL, соединяя базовый URL с относительным путем.
        :param path: Относительный путь.
        :return: Полный URL.
        """
        if self.base_url:
            return urljoin(self.base_url, path)
        return path

    @allure.step('Making GET request to "{url}"')
    def get(
        self,
        url: URLTypes,
        *,
        params: QueryParamTypes = None,
        headers: HeaderTypes = None,
        cookies: CookieTypes = None,
        auth: typing.Optional[AuthBase] = None,
        follow_redirects: bool = True,
        timeout: TimeoutTypes = None,
    ) -> Response:
        """
        Выполняет HTTP GET-запрос.
        :param url: URL для запроса.
        :param params: Параметры запроса.
        :param headers: Заголовки запроса.
        :param cookies: Cookies для запроса.
        :param auth: Данные для аутентификации.
        :param follow_redirects: Флаг для следования по редиректам.
        :param timeout: Таймаут запроса.
        :return: Объект Response от сервера.
        """
        url = self._full_url(url)
        return self.session.get(
            url,
            params=params,
            headers=headers,
            cookies=cookies,
            auth=auth,
            allow_redirects=follow_redirects,
            timeout=timeout
        )

    @allure.step('Making POST request to "{url}"')
    def post(
        self,
        url: URLTypes,
        *,
        data: RequestData = None,
        files: RequestFiles = None,
        json: typing.Optional[typing.Any] = None,
        params: QueryParamTypes = None,
        headers: HeaderTypes = None,
        cookies: CookieTypes = None,
        auth: typing.Optional[AuthBase] = None,
        follow_redirects: bool = True,
        timeout: TimeoutTypes = None,
    ) -> Response:
        """
        Выполняет HTTP POST-запрос.
        :param url: URL для запроса.
        :param params: Параметры запроса.
        :param headers: Заголовки запроса.
        :param cookies: Cookies для запроса.
        :param auth: Данные для аутентификации.
        :param follow_redirects: Флаг для следования по редиректам.
        :param timeout: Таймаут запроса.
        :return: Объект Response от сервера.
        """
        url = self._full_url(url)
        return self.session.post(
            url,
            data=data,
            files=files,
            json=json,
            params=params,
            headers=headers,
            cookies=cookies,
            auth=auth,
            allow_redirects=follow_redirects,
            timeout=timeout
        )

    @allure.step('Making PUT request to "{url}"')
    def put(
        self,
        url: URLTypes,
        *,
        data: RequestData = None,
        files: RequestFiles = None,
        json: typing.Optional[typing.Any] = None,
        params: QueryParamTypes = None,
        headers: HeaderTypes = None,
        cookies: CookieTypes = None,
        auth: typing.Optional[AuthBase] = None,
        follow_redirects: bool = True,
        timeout: TimeoutTypes = None,
    ) -> Response:
        """
        Выполняет HTTP PUT-запрос.
        :param url: URL для запроса.
        :param params: Параметры запроса.
        :param headers: Заголовки запроса.
        :param cookies: Cookies для запроса.
        :param auth: Данные для аутентификации.
        :param follow_redirects: Флаг для следования по редиректам.
        :param timeout: Таймаут запроса.
        :return: Объект Response от сервера.
        """
        url = self._full_url(url)
        return self.session.put(
            url,
            data=data,
            files=files,
            json=json,
            params=params,
            headers=headers,
            cookies=cookies,
            auth=auth,
            allow_redirects=follow_redirects,
            timeout=timeout
        )

    @allure.step('Making DELETE request to "{url}"')
    def delete(
        self,
        url: URLTypes,
        *,
        params: QueryParamTypes = None,
        headers: HeaderTypes = None,
        cookies: CookieTypes = None,
        auth: typing.Optional[AuthBase] = None,
        follow_redirects: bool = True,
        timeout: TimeoutTypes = None,
    ) -> Response:
        """
        Выполняет HTTP DELETE-запрос.
        :param url: URL для запроса.
        :param params: Параметры запроса.
        :param headers: Заголовки запроса.
        :param cookies: Cookies для запроса.
        :param auth: Данные для аутентификации.
        :param follow_redirects: Флаг для следования по редиректам.
        :param timeout: Таймаут запроса.
        :return: Объект Response от сервера.
        """
        url = self._full_url(url)
        return self.session.delete(
            url,
            params=params,
            headers=headers,
            cookies=cookies,
            auth=auth,
            allow_redirects=follow_redirects,
            timeout=timeout
        )

class APIClient:
    def __init__(self, client: HTTPClient) -> None:
        """
        Инициализация API-клиента с HTTP-клиентом.
        :param client: Экземпляр HTTPClient.
        """
        self._client = client

    @property
    def client(self) -> HTTPClient:
        """
        Возвращает HTTP-клиент, связанный с API-клиентом.
        :return: Экземпляр HTTPClient.
        """
        return self._client