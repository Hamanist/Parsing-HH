import os
from dotenv import load_dotenv
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

load_dotenv()


def create_database() -> None:
    """Создание БД если ее Нет"""

    db_name = os.getenv('DB_NAME')
    if not db_name:
        raise ValueError(f'Переменная DB_NAME не найдена')

    conn = None
    cur = None
    try:
        # Подключаемся к служебной БД 'postgres'
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database="postgres"
        )
        # Устанавливаем автокоммит — иначе будет ошибка
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()

        # Проверяем, существует ли БД с таким именем
        cur.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s", (db_name,))
        if not cur.fetchone():
            cur.execute(f'CREATE DATABASE "{db_name}"')


    except psycopg2.Error as e:
        raise RuntimeError(f"Ошибка при создании базы данных '{db_name}': {e}") from e


    finally:
        # Всегда закрываем курсор и соединение
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()


def create_table() -> None:
    """
    Создаём таблицы 'employers' и 'vacancies' в базе данных.
    """
    conn_params = {
        'host': os.getenv('DB_HOST'),
        'port': os.getenv('DB_PORT'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'database': os.getenv('DB_NAME')
    }

    with psycopg2.connect(**conn_params) as conn:
        with conn.cursor() as cur:
            # Таблица компаний
            cur.execute(
            """CREATE TABLE IF NOT EXISTS employers (
                employer_id INTEGER PRIMARY KEY,
                name VARCHAR(255) NOT NULL
            )"""
            )

            # Таблица вакансий
            cur.execute(
                """CREATE TABLE IF NOT EXISTS vacancies (
                vacancy_id SERIAL PRIMARY KEY,
                employer_id INTEGER NOT NULL REFERENCES employers(employer_id) ON DELETE CASCADE,
                url TEXT,
                area VARCHAR(80),
                profession VARCHAR(255),
                experience VARCHAR(150),
                salary_min VARCHAR(50),
                salary_max VARCHAR(50),
                requirement TEXT,
                responsibilities TEXT
                )"""
            )
