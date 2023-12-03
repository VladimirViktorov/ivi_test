from enum import Enum

class URL(str, Enum):
    MAIN = 'http://rest.test.ivi.ru'
    
    def __str__(self) -> str:
        return self.value

API_VERSION = '/v2'  # Задаем версию API как константу

class APIRoutes():
    CHARACTERS = API_VERSION + '/characters'
    CHARACTER = API_VERSION + '/character'
    RESET = API_VERSION + '/reset'
    
    def __str__(self) -> str:
        return self.value

class APIErrors():
    INVALID_AUTHENTICATION = 'You have to login with proper credentials'