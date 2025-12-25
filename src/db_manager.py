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
        with psycopg2.connect(**self.conn_params) as conn:
            with conn.cursor() as cur:
                for emp in employers:
                    cur.execute("INSERT INTO employers (employer_id, name) VALUES (%s, %s) ON CONFLICT DO NOTHING",
                                (emp['id'], emp['company'])
                                )

    def get_companies_and_vacancies_count(self): ...

    # — список всех компаний и количество вакансий у каждой компании
    def get_all_vacancies(self): ...

    # — список всех вакансий с указанием названия компании, вакансии, зарплаты и ссылки
    def get_avg_salary(self): ...

    # — средняя зарплата по вакансиям
    def get_vacancies_with_higher_salary(self): ...

    # — список вакансий с зарплатой выше средней
    def get_vacancies_with_keyword(self): ...
    # — список вакансий, в названии которых содержатся переданные слова


db = DBManager()
print(db.insert_employers(ParseHH().get_data_via_API()))
