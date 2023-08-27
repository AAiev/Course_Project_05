from src.utils import get_request, create_database, save_data_in_database
from src.DBManager import DBManager
from src.config import config
from pprint import pprint

NAME_DATABASE = 'hh_ru_vacancies'
EMPLOYER_ID = [1740, 2126550]


def main():
    user_input = input('1 - загрузить вакансии с сайта HH.RU заново.\n'
                       '2 - работать с вакансиями, загруженными ранее\n')
    params = config()
    if user_input == 1:

        # api запрос вакансий с HH.RU
        list_vacancies = []
        for emp_id in EMPLOYER_ID:
            vacancies = get_request(emp_id)
            list_vacancies.append(vacancies)
        # pprint(list_vacancies)


        # создаем базу данных

        create_database(NAME_DATABASE, params)

        # сохраняем данные из полученного запроса в базу данных
        save_data_in_database(list_vacancies, NAME_DATABASE, params)

    db1 = DBManager(NAME_DATABASE, params)

    db1.get_companies_and_vacancies_count()


if __name__ == '__main__':
    main()
