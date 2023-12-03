from enum import Enum
from string import Template

class URL(str, Enum):
    MAIN = "http://rest.test.ivi.ru"
    
    def __str__(self) -> str:
        return self.value

API_VERSION = "/v2"  # Задаем версию API как константу

class APIRoutes():
    CHARACTERS = API_VERSION + "/characters"
    CHARACTER = API_VERSION + "/character"
    RESET = API_VERSION + "/reset"
    
    def __str__(self) -> str:
        return self.value

class APIResults():
    DELETE_CHARACTER = Template("Hero $name is deleted")

class APIErrors():
    INVALID_AUTHENTICATION = "You have to login with proper credentials"
    NO_SUCH_NAME = "No such name"
    COLLECTION_500_ITEMS = "Collection can't contain more than 500 items"
    MISSING_NAME = "name: ['Missing data for required field.']"
    ALREADY_EXISTS = Template("$name is already exists")
    INVALID_JSON = "Payload must be a valid json"
    INVALID_SCHEMA = "_schema: ['Invalid input type.']"
    INVALID_DATA = {"name": "name: ['Not a valid string.']",
                    "universe": "universe: ['Not a valid string.']",
                    "education": "education: ['Not a valid string.']",
                    "other_aliases": "other_aliases: ['Not a valid string.']",
                    "weight": "weight: ['Not a valid number.']",
                    "height": "height: ['Not a valid number.']",
                    "identity": "identity: ['Not a valid string.']"}
    NULL_DATA = {"name": "name: ['Field may not be null.']",
                 "universe": "universe: ['Field may not be null.']",
                 "education": "education: ['Field may not be null.']",
                 "other_aliases": "other_aliases: ['Field may not be null.']",
                 "weight": "weight: ['Field may not be null.']",
                 "height": "height: ['Field may not be null.']",
                 "identity": "identity: ['Field may not be null.']"}
    EXTRA_DATA = {"name": "name: ['Length must be between 1 and 350.']",
                 "universe": "universe: ['Length must be between 1 and 350.']",
                 "education": "education: ['Length must be between 1 and 350.']",
                 "other_aliases": "other_aliases: ['Length must be between 1 and 350.']",
                 "weight": "weight: ['Number too large.']",
                 "height": "height: ['Number too large.']",
                 "identity": "identity: ['Length must be between 1 and 350.']"}