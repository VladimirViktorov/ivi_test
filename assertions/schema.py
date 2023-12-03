import allure
from jsonschema import validate
from jsonschema import Draft7Validator


@allure.step('Validating schema')
def validate_schema(instance: dict, schema: dict) -> None:
    validate(instance=instance, schema=schema)

@allure.step('Validating data')
def validate_data(schema: dict, data: dict) -> list:
    validator = Draft7Validator(schema)
    errors = sorted(validator.iter_errors(data), key=lambda e: e.path)
    invalid_fields = [list(e.path)[-1] for e in errors if e.path]
    return invalid_fields if invalid_fields else None

@allure.step('Check change data')
def check_change_data(original_data: dict, updated_data: dict, body: dict):
    # Проверяем, что поля, указанные в body, изменились
    for key in body:
        if key != 'name':
            assert key in updated_data, f"Key {key} not found in updated data"
            assert updated_data[key] == body[key], f"Field {key} did not update correctly. Expected: {body[key]}, Got: {updated_data[key]}"
    
    # Проверяем, что другие поля не изменились
    for key in original_data:
        if key not in body and key != 'name':
            assert key in updated_data, f"Key {key} not found in updated data"
            assert updated_data[key] == original_data[key], f"Field {key} changed unexpectedly. Original: {original_data[key]}, Updated: {updated_data[key]}"