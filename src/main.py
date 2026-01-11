from src.api_connector import ParseHH
from src.db_creator import create_database, create_table
from src.db_manager import DBManager


def main():
    """
    Точка входа для взаимодействия с пользователем.

    """
    # создание БД и таблицы
    create_database()
    create_table()

    # получаем список словарей из HH
    parse_hh = ParseHH()
    try:
        raw_data = parse_hh.get_data_via_API()
    except Exception as e:
        print(f"❌ Ошибка при получении данных: {e}")
        return
    # подключаемся к БД и заполняем таблицы
    db = DBManager()
    db.insert_employers(raw_data)
    db.insert_vacancies(raw_data)

    # взаимодействия с пользователем

    while True:
        print('\nВыберите действие')
        print('1 - Список компаний и количество вакансий')
        print('2 - Список всех вакансий')
        print('3 - Средние зарплаты')
        print('4 - Вакансий с зарплатой выше средней')
        print('5 - Вакансии по ключевым словам')
        print('0 - для выхода\n')

        choice = input('Введите номер действия: ').strip()

        if choice == '1':
            for company, count in db.get_companies_and_vacancies_count():
                print(f'{company}, количество вакансий {count}\n')

        elif choice == '2':
            for data in db.get_all_vacancies():
                company, profession, salary_min, salary_max, url = data
                min_str = str(salary_min) if salary_min is not None else 'Не указана'
                max_str = str(salary_max) if salary_max is not None else 'Не указана'
                print(f'{company} | {profession}, Зарплата от {min_str} до {max_str}\n')

        elif choice == '3':
            for company, agv_salary in db.get_avg_salary():
                print(f'{company}, средние зарплаты {agv_salary}\n')

        elif choice == '4':
            for company, profession, avg_salary in db.get_vacancies_with_higher_salary():
                print(f'{company} | {profession} | Зарплата {avg_salary}\n')

        elif choice == '5':
            keyword = input('Введите ключевое слово - ')
            for data in db.get_vacancies_with_keyword(keyword):
                company, area, profession, experience, salary_min, salary_max, requirement, responsibilities, url = data
                min_str = str(salary_min) if salary_min is not None else 'Не указана'
                max_str = str(salary_max) if salary_max is not None else 'Не указана'

                print(f"""Компания {company}, Город {area}
Профессия {profession} | опыт {experience},
Зарплата от {min_str} до {max_str},
Требование {requirement},
Обязанности {responsibilities},
url-адрес{url}\n""")

        elif choice == '0':
            print('\nВсего доброго!')
            break

        else:
            print('Неверный выбор. Попробуйте снова.')


if __name__ == "__main__":
    main()
