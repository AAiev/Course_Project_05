import requests
import json
import psycopg2

class ParsingError(Exception):
    """Общий класс для API"""

    def __init__(self, *args):
        self.message = args[0] if args else 'Ошибка получения вакансий.'

    def __str__(self):
        return self.message


def get_request(employer_id=None, url='https://api.hh.ru/vacancies'):
    """Запрос по API"""
    list_vacancies = []
    for n in range(0, 20):
        params = {"per_page": 100,
                  "page": 0 + n,
                  "employer_id": employer_id
                  }
        req = requests.get(url, params)
        if req:
            data_req = req.content.decode()  # Декодируем его ответ, чтобы Кириллица отображалась корректно
            json_obj = json.loads(data_req)
            list_vacancies += json_obj['items']
        else:
            break

    if req.status_code != 200:
        raise ParsingError(f'Ошибка получения вакансий. Код статуса: {req.status_code}')
    else:
        return list_vacancies

def create_database(NAME_DATABASE: str, params: dict):
    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute(f"DROP DATABASE IF EXISTS {NAME_DATABASE}")
    cur.execute(f"CREATE DATABASE {NAME_DATABASE}")

    conn.close()

    conn = psycopg2.connect(dbname=NAME_DATABASE, **params)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE companies (
                company_id SERIAL PRIMARY KEY, 
                company_name VARCHAR NOT NULL
            )
        """)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE vacancies (
                vacancy_id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                company_id INT REFERENCES companies(company_id),
                salary_from INTEGER,
                salary_to INTEGER,
                salary_currency VARCHAR,
                url TEXT
            )
        """)

    conn.commit()
    conn.close()

def save_data_in_database(list_vacancies:list[list[dict]], NAME_DATABASE, params):
    conn = psycopg2.connect(dbname=NAME_DATABASE, **params)

    with conn.cursor() as cur:
        for vacancy in list_vacancies:
            data_company = vacancy[0]
            cur.execute("""
            INSERT INTO companies (company_id, company_name)
            VALUES (%s, %s)
            """,
            (data_company['employer']['id'], data_company['employer']['name'])
            )

    with conn.cursor() as cur:
        for vacancies_company in list_vacancies:
            for data_vacancy in vacancies_company:
                if data_vacancy['salary'] == None:
                    salary_from = 0
                    salary_to = 0
                    salary_currency = 'RUR'
                elif data_vacancy['salary']['from'] == None:
                    salary_from = 0
                    salary_to = data_vacancy['salary']['to']
                    salary_currency = data_vacancy['salary']['currency']
                elif data_vacancy['salary']['to'] == None:
                    salary_from = data_vacancy['salary']['from']
                    salary_to = 0
                    salary_currency = data_vacancy['salary']['currency']
                else:
                    salary_from = data_vacancy['salary']['from']
                    salary_to = data_vacancy['salary']['to']
                    salary_currency = data_vacancy['salary']['currency']
                cur.execute("""
                INSERT INTO vacancies (vacancy_id, name, 
                company_id, 
                salary_from, salary_to, 
                salary_currency, url)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (data_vacancy['id'], data_vacancy['name'],
                 data_vacancy['employer']['id'],
                 salary_from, salary_to,
                 salary_currency, data_vacancy['alternate_url'])
                )

    conn.commit()
    conn.close()