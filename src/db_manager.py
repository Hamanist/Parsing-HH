import os
import psycopg2
from dotenv import load_dotenv

from src.api_connector import ParseHH

load_dotenv()


class DBManager:
    def __init__(self):
        self.conn_params = {
            'host': os.getenv('DB_HOST'),
            'port': os.getenv('DB_PORT'),
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASSWORD'),
            'database': os.getenv('DB_NAME')
        }

    def insert_employers(self, employers: list[dict]) -> None:
        """
        Метод добавляет данные в таблицу employers
        ON CONFLICT DO NOTHING - безопасный способ вставки, который предотвращает ошибки дублирования по уникальному ключу.
        """
        with psycopg2.connect(**self.conn_params) as conn:
            with conn.cursor() as cur:
                for emp in employers:
                    cur.execute("INSERT INTO employers (employer_id, name) VALUES (%s, %s) ON CONFLICT DO NOTHING",
                                (emp['id'], emp['company'])
                                )

    def insert_vacancies(self, vacancies: list[dict]) -> None:
        """
        Метод добавляет данные в таблицу vacancies
        """
        with psycopg2.connect(**self.conn_params) as conn:
            with conn.cursor() as cur:
                for vac in vacancies:
                    cur.execute("""INSERT INTO vacancies (
                    employer_id, url, area, profession, experience,
                    salary_min, salary_max, requirement, responsibilities)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                                (vac['id'], vac['url'], vac['area'], vac['profession'], vac['experience'],
                                 vac['salary_min'], vac['salary_max'], vac['requirement'], vac['responsibilities'])
                                )

    def get_companies_and_vacancies_count(self) -> list[tuple[str, int]]:
        """ Список всех компаний и количество вакансий у каждой компании
            return - данные в виде (Компания и количество вакансий)
        """
        with psycopg2.connect(**self.conn_params) as conn:
            with conn.cursor() as cur:
                cur.execute("""SELECT e.name, COUNT(v.employer_id) AS vacancies_count FROM employers e
                            LEFT JOIN vacancies v ON e.employer_id = v.employer_id
                            GROUP BY e.employer_id, e.name
                            ORDER BY vacancies_count DESC""")

                return cur.fetchall()

    def get_all_vacancies(self):
        """ список всех вакансий с указанием названия
            компании, вакансии, зарплаты и ссылки"""

        with psycopg2.connect(**self.conn_params) as conn:
            with conn.cursor() as cur:
                cur.execute("""SELECT e.name, v.profession, v.salary_min, v.salary_max, v.url FROM employers e
                            JOIN vacancies v USING(employer_id)
                            ORDER BY e.name""")
                return cur.fetchall()

    def get_avg_salary(self):
        """Средняя зарплата по вакансиям

            Возвращает вакансии, где указана и минимальная, и максимальная зарплата.
            Средняя зарплата рассчитывается как (min + max) / 2.
            Вакансии с частично указанной зарплатой исключаются.
            """
        with psycopg2.connect(**self.conn_params) as conn:
            with conn.cursor() as cur:
                cur.execute("""SELECT e.name,
                            (salary_min + salary_max) / 2
                            FROM employers e
                            JOIN vacancies v USING(employer_id)
                            WHERE salary_min IS NOT NULL AND salary_max IS NOT NULL
                            ORDER BY e.name""")
                return cur.fetchall()

    def get_vacancies_with_higher_salary(self):
        """ Список вакансий с зарплатой выше средней.
            Получает список вакансий, у которых средняя зарплата (min+max)/2
            выше средней зарплаты по всем вакансиям (где указаны и min, и max).
        """
        with psycopg2.connect(**self.conn_params) as conn:
            with conn.cursor() as cur:
                cur.execute("""SELECT
	                                e.name,
	                                v.profession,
	                                (v.salary_min + v.salary_max) / 2 AS avg_salary,
	                            FROM employers e
                                JOIN vacancies v USING(employer_id)

                                WHERE v.salary_min IS NOT NULL AND v.salary_max IS NOT NULL
	                                AND (v.salary_min + v.salary_max) / 2 > (SELECT AVG((v2.salary_min + v2.salary_max) / 2)
	                                FROM vacancies v2
	                                WHERE v2.salary_min IS NOT NULL AND v2.salary_max IS NOT NULL)
                                ORDER BY avg_salary DESC""")

    def get_vacancies_with_keyword(self):
        """список вакансий, в названии которых содержатся переданные слова"""
        pass


db = DBManager()
# db.insert_employers(ParseHH().get_data_via_API())
# db.insert_vacancies(ParseHH().get_data_via_API())
# print(db.get_companies_and_vacancies_count(), sep='\n')
print(*db.get_avg_salary(), sep='\n')
