import psycopg2
import os
from src.api import HeadHunterAPI


class DBManager:
    """
    Класс для работы с базами данных по работодателям и их вакансиям.
    """
    def __init__(self):
        pass

    def create_db(self, companies):
        hh_api = HeadHunterAPI()
        with psycopg2.connect(host=os.getenv('POSTGRES_HOST'), database=os.getenv('POSTGRES_DB'),
                              user=os.getenv('POSTGRES_USER'), password=os.getenv('POSTGRES_PASS')) as conn:
            with conn.cursor() as cur:
                cur.execute(f"DROP TABLE IF EXISTS employers CASCADE;"
                            f"DROP TABLE IF EXISTS vacancies CASCADE;"
                            f"CREATE TABLE employers (employer_id int PRIMARY KEY, emp_name varchar(50), "
                            f"open_vacancies int, emp_url varchar(50));")
                cur.execute(f"CREATE TABLE vacancies (vacancy_id int PRIMARY KEY, "
                            f"employer_id int REFERENCES employers(employer_id), vac_name varchar(100),"
                            f"salary int, salary_cur varchar(10), vac_url varchar(50));")
                for item in companies:
                    data_emp = hh_api.get_employer(item)
                    cur.execute(f"INSERT INTO employers VALUES({data_emp['employer_id']}, '{data_emp['name']}', "
                                f"{data_emp['open_vacancies']}, '{data_emp['url']}')")
                    data_vac = hh_api.get_vacancies(item)
                    for i in data_vac:
                        cur.execute(f"INSERT INTO vacancies VALUES({i['vacancy_id']}, {i['employer_id']},"
                                    f"'{i['name']}', {i['salary']}, '{i['salary_currency']}', "
                                    f"'{i['url']}')")

    def get_companies_and_vacancies_count(self):
        """Получает список всех компаний и количество вакансий у каждой."""
        with psycopg2.connect(host=os.getenv('POSTGRES_HOST'), database=os.getenv('POSTGRES_DB'),
                              user=os.getenv('POSTGRES_USER'), password=os.getenv('POSTGRES_PASS')) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT emp_name, open_vacancies FROM employers")
                rows = cur.fetchall()
                for row in rows:
                    print(row)

    def get_all_vacancies(self):
        """Получает список всех вакансий с указанием названия компании, названия вакансии, зарплаты и ссылки."""
        with psycopg2.connect(host=os.getenv('POSTGRES_HOST'), database=os.getenv('POSTGRES_DB'),
                              user=os.getenv('POSTGRES_USER'), password=os.getenv('POSTGRES_PASS')) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT employers.emp_name, vac_name, salary, vac_url FROM vacancies "
                            "JOIN employers USING(employer_id)")
                rows = cur.fetchall()
                for row in rows:
                    print(row)

    def get_avg_salary(self):
        """Получает среднюю зарплату по вакансиям."""
        with psycopg2.connect(host=os.getenv('POSTGRES_HOST'), database=os.getenv('POSTGRES_DB'),
                              user=os.getenv('POSTGRES_USER'), password=os.getenv('POSTGRES_PASS')) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT AVG(salary) from vacancies "
                            "WHERE salary > 0")
                rows = cur.fetchall()
                print(rows[0][0])

    def get_vacancies_with_higher_salary(self):
        """Получает список всех вакансий, у которых зарплата выше средней."""
        with psycopg2.connect(host=os.getenv('POSTGRES_HOST'), database=os.getenv('POSTGRES_DB'),
                              user=os.getenv('POSTGRES_USER'), password=os.getenv('POSTGRES_PASS')) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT employers.emp_name, vac_name, salary, vac_url FROM vacancies "
                            "JOIN employers USING(employer_id) "
                            "WHERE salary > (SELECT AVG(salary) from vacancies WHERE salary > 0)")
                rows = cur.fetchall()
                for row in rows:
                    print(row)

    def get_vacancies_with_keyword(self, keyword):
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова."""
        with psycopg2.connect(host=os.getenv('POSTGRES_HOST'), database=os.getenv('POSTGRES_DB'),
                              user=os.getenv('POSTGRES_USER'), password=os.getenv('POSTGRES_PASS')) as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT employers.emp_name, vac_name, salary, vac_url FROM vacancies "
                            f"JOIN employers USING(employer_id) "
                            f"WHERE vac_name LIKE '%{keyword}%'")
                rows = cur.fetchall()
                for row in rows:
                    print(row)
