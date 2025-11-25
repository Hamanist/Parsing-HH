from pprint import pprint
from typing import Any

import requests


class Parse_HH:
    """
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
            СБЕР]
    """
    __url = 'https://api.hh.ru/vacancies'
    __employer_id = [58320, 2748, 4181, 10477195, 9498112, 1420559, 1793216, 697715, 6836, 3529]

    def get_data_via_API(self) -> int | Any:
        """
        Получить данные через API
        :return:
        """
        __params = {
            "employer_id": self.__employer_id,
            'per_page': '10'
        }

        response = requests.get(url=self.__url, params=__params)
        if response.status_code == 200:
            return self._parse(response.json())
        else:
            return response.status_code

