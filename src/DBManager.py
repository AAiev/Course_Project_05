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
                print(f'В компании "{row[0]}" - {row[1]} вакансий.')

    def get_all_vacancies(self):
        """
        получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.
        """
        conn = psycopg2.connect(dbname=self.name_database, **self.params)
        with conn.cursor() as cur:
            cur.execute('SELECT companies.company_name, vacancy_name, ((salary_from + salary_to)/2) AS salary, vacancy_url '
                        'FROM vacancies '
                        'INNER JOIN companies '
                        'USING (company_id) '
                        "WHERE ((salary_from + salary_to)/2) > 0 AND salary_currency = "RUR"')
                        'ORDER BY salary DESC')
            rows = cur.fetchall()
            for row in rows:
                print(f'В компании "{row[0]}" имеется вакансия "{row[1]}".'
                      f'Зарплата - {row[2]}. Ссылка на вакансию: {row[3]}')

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