import psycopg2


class DBManager:
    def __init__(self, name_database, params):
        self.name_database = name_database
        self.params = params

    def get_companies_and_vacancies_count(self):
        """
        получает список всех компаний и количество вакансий у каждой компании.
        """

        conn = psycopg2.connect(dbname=self.name_database, **self.params)
        with conn.cursor() as cur:
            cur.execute('SELECT company_name, COUNT(*) AS "Кол-во вакансий" '
                        'FROM companies '
                        'INNER JOIN vacancies '
                        'USING(company_id) GROUP BY company_id '
                        'ORDER BY "Кол-во вакансий" DESC')
            rows = cur.fetchall()
            for row in rows:
                print(row)

    def get_all_vacancies(self):
        """
        получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.
        """
        pass

    def get_avg_salary(self):
        """
        получает среднюю зарплату по вакансиям.
        """
        pass

    def get_vacancies_with_higher_salary(self):
        """
        получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
        """
        pass

    def get_vacancies_with_keyword(self):
        """
        получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python.
        """
        pass