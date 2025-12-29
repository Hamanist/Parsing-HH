from pprint import pprint
from typing import Any, Tuple, Union, List, Dict

import requests


class ParseHH:
    """
    Класс для парсинга нужных нам полей из HH.
    Вернет список валидных полей для заполнения ими БД.
    __url - поиск по HH
    __employer_id - список компаний
            [Россельхозбанк,
            ПАО Ростелеком,
            Банк ВТБ (ПАО),
            ООО Самолет Плюс,
            Яндекс Крауд,
            Веза,
            Солар,
            Островок,
            Fplus,
            СБЕР,
            Wiren Board,
            Procter & Gamble,
            WILDBERRIES]
    """
    __url = 'https://api.hh.ru/vacancies'
    __employer_id = [58320, 2748, 4181, 10477195, 9498112, 1420559, 1793216, 697715, 6836, 3529, 1995794, 4949, 87021]

    @staticmethod
    def salary_check(salary_data: dict | None) -> Tuple[Union[int, None], Union[int, None]]:
        """
        Проверка зарплат на None.
        Метод будет использоваться в методе (_parse_vacancies)
        :param salary_data: Указана или не указана зарплата
        :return: Если не казана выводит (Не указана), в другом случае выводит зарплату
        """
        if salary_data is None:
            return None, None

        return (
            salary_data.get('from'),  # вернёт int или None
            salary_data.get('to')  # вернёт int или None
        )

    def get_data_via_API(self) -> list[dict[str, str | int]] | str:
        """
        Получить данные через API
        :return: Список, где хранятся словари с данными.
        """
        __params = {
            "employer_id": self.__employer_id,
            'per_page': '100'
        }

        response = requests.get(url=self.__url, params=__params)
        if response.status_code == 200:
            return self._parse_vacancies(response.json())
        else:
            return f'Код ошибки: {response.status_code}'

    def _parse_vacancies(self, data) -> List[Dict[str, Union[str, int, None]]]:
        """

        :param data: ответ (response.json()) с метода get_data_via_API для парсинга
        :return: Список данных с парсинга
        """
        answers = []
        for vacancies in data['items']:
            salary_min, salary_max = self.salary_check(vacancies['salary'])

            answers.append({
                'id': vacancies['employer']['id'],
                'company': vacancies['employer']['name'],
                'requirement': vacancies['snippet']['requirement'],
                'responsibilities': vacancies['snippet']['responsibility'],
                'url': vacancies['alternate_url'],
                'area': vacancies['area']['name'],
                'profession': vacancies['name'],
                'experience': vacancies['experience']['name'],
                'salary_min': salary_min,
                'salary_max': salary_max
            })
        return answers
