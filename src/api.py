from abc import ABC, abstractmethod
import requests
import json


class API(ABC):
    """
    Абстрактный класс для взаимодействия с API сайта вакансий
    """

    @abstractmethod
    def get_employer(self, employer_id):
        pass

    @abstractmethod
    def get_vacancies(self, employer_id):
        pass


class HeadHunterAPI(API):
    """
    Класс для взаимодействия с API HeadHunter
    """

    def __init__(self):
        pass

    def get_employer(self, employer_id):
        """Получение описаний работодателей через API по идентификатору"""
        resp = json.loads(requests.get(f'https://api.hh.ru/employers/{str(employer_id)}').content.decode())
        result = {'employer_id': employer_id, 'name': resp['name'], 'open_vacancies': resp['open_vacancies'],
                  'url': resp['alternate_url']}
        return result

    def get_vacancies(self, employer_id):
        """Получение вакансий через API по идентификатору работодателя"""
        resp = json.loads(requests.get('https://api.hh.ru/vacancies',
                                       params={'page': 0, 'per_page': 10,
                                               'employer_id': str(employer_id)}).content.decode())['items']
        result = []
        for item in resp:
            if not item['salary']:
                salary = 0
                salary_currency = ''
            else:
                if not item['salary']['from']:
                    salary = int(item['salary']['to'])
                elif not item['salary']['to']:
                    salary = int(item["salary"]["from"])
                else:
                    salary = int(item['salary']['to'])
                if not item['salary']['currency']:
                    salary_currency = ''
                else:
                    salary_currency = item['salary']['currency']
            result.append({'vacancy_id': int(item['id']), 'name': item['name'], 'salary': salary,
                           'salary_currency': salary_currency, 'url': item['alternate_url'],
                           'employer_id': int(item['employer']['id'])})
        return result
