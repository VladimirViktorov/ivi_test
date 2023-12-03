from jsonschema import validate
import jsonschema

class SCHEMES:
    CharactersDict = {
        "type": "object",
        "properties": {
            "result": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "education": {"type": ["string", "null"]},
                        "height": {"type": ["number", "null"]},
                        "identity": {"type": ["string", "null"]},
                        "name": {"type": "string"},
                        "other_aliases": {"type": ["string", "null"]},
                        "universe": {"type": ["string", "null"]},
                        "weight": {"type": ["number", "null"]}
                    },
                    "required": ["name"],
                    "additionalProperties": False
                }
            }
        },
        "required": ["result"],
        "additionalProperties": False
    }