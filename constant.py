from string import Template

class URL():
    MAIN = 'rest.test.ivi.ru/v2'
    CHARACTERS = '/characters'
    CHARACTER = Template('/character?name=$name')
    RESET = '/reset'