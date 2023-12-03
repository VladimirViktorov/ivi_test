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
        self.session = requests.Session()
        if base_url:
            self.base_url = base_url
        
        if username and password:
            self.session.auth = HTTPBasicAuth(username, password)
    
    def _full_url(self, path):
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
    
    @allure.step('Making PATCH request to "{url}"')
    def patch(
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
        url = self._full_url(url)
        return self.session.patch(
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
        self._client = client

    @property
    def client(self) -> HTTPClient:
        return self._client