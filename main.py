import psycopg2
from src.utils import get_request, create_database, save_data_in_database
from src.DBManager import DBManager
from src.config import config


NAME_DATABASE = 'hh_ru_vacancies'
EMPLOYER_ID = [1740, 2126550, 78638]


def main():
    try:
        while True:
            user_input = input('1 - загрузить вакансии с сайта HH.RU заново.\n'
                           '2 - работать с вакансиями, загруженными ранее\n')
            params = config()
            if user_input == '1':
                # api запрос вакансий с HH.RU
                list_vacancies = []
                for emp_id in EMPLOYER_ID:
                    vacancies = get_request(emp_id)
                    list_vacancies.append(vacancies)
                quantity_companies = len(list_vacancies)
                quantity_vacancies = sum([len(i) for i in list_vacancies])
                print(f'Загружено {quantity_vacancies} вакансий по {quantity_companies} компаниям.')
                # создаем базу данных
                create_database(NAME_DATABASE, params)
                # сохраняем данные из полученного запроса в базу данных
                save_data_in_database(list_vacancies, NAME_DATABASE, params)
                break
            elif user_input == '2':
                break
            else:
                print('Недействительный ответ')

        while True:
            user_input_2 = input('Выбери нужный пункт:\n'
                                 '1 - Вывести список всех компаний и количество вакансий у каждой компании\n'
                                 '2 - Вывести список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию\n'
                                 '3 - Вывести среднюю зарплату по вакансиям\n'
                                 '4 - Вывести список всех вакансий, у которых зарплата выше средней по всем вакансиям\n'
                                 '5 - Вывести список всех вакансий, по ключевому слову\n'
                                 'для выхода введи стоп\n')

            db1 = DBManager(NAME_DATABASE, params)
            if user_input_2 == '1':
                db1.get_companies_and_vacancies_count()
                print()
            elif user_input_2 == '2':
                db1.get_all_vacancies()
                print()
            elif user_input_2 == '3':
                db1.get_avg_salary()
                print()
            elif user_input_2 == '4':
                db1.get_vacancies_with_higher_salary()
                print()
            elif user_input_2 == '5':
                word_input = input('Введите ключевое слово:\n')
                db1.get_vacancies_with_keyword(word_input)
                print()
            elif user_input_2.lower() == 'stop' or user_input_2.lower() == 'стоп':
                break
    except psycopg2.OperationalError:
        print('Не удалось подключиться к базе. Возможно база не найдена. Загрузите базу заново.')


if __name__ == '__main__':
    main()
