import requests
import json

class ParsingError(Exception):
    """Общий класс для API"""

    def __init__(self, *args):
        self.message = args[0] if args else 'Ошибка получения вакансий.'

    def __str__(self):
        return self.message


def get_request(employer_id=None, url='https://api.hh.ru/vacancies'):
    """Запрос по API"""
    params = {"per_page": 100,
              "page": 0,
              "employer_id": employer_id
              }
    req = requests.get(url, params)
    data_req = req.content.decode()  # Декодируем его ответ, чтобы Кириллица отображалась корректно
    json_obj = json.loads(data_req)
    if req.status_code != 200:
        raise ParsingError(f'Ошибка получения вакансий. Код статуса: {req.status_code}')
    else:
        return json_obj

def create_database(NAME_DATABASE, params):
    pass

def save_data_in_database(list_vacancies, NAME_DATABASE, params):
    pass