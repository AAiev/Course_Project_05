from src.utils import get_request, create_database, save_data_in_database
from src.DBManager import DBManager
from src.config import config
from pprint import pprint

NAME_DATABASE = 'hh_ru_vacancies'
EMPLOYER_ID = [1740]


def main():
    # api запрос вакансий с HH.RU
     = []
    for id in EMPLOYER_ID:
        vacancies = get_request(id)
        list_vacancies.append(vacancies)






if __name__ == '__main__':
    main()