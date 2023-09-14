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
        resp = json.loads(requests.get('https://api.hh.ru/employers',
                                       params={'page': 0, 'per_page': 100,
                                               'employer_id': str(employer_id)}).content.decode())['items']
        result = []
        for item in resp:
            result.append({'name': item['name'], 'open_vacancies': ,
                           'url': item['alternate_url']})
        return result

    def get_vacancies(self, employer_id):
        """Получение вакансий через API по идентификатору работодателя"""
        resp = json.loads(requests.get('https://api.hh.ru/vacancies',
                                       params={'page': 0, 'per_page': 100,
                                               'employer_id': str(employer_id)}).content.decode())['items']
        result = []
        for item in resp:
            if not item['salary']:
                salary_from = None
                salary_to = None
                salary_currency = None
            else:
                if not item['salary']['from']:
                    salary_from = None
                    salary_to = int(item['salary']['to'])
                elif not item['salary']['to']:
                    salary_from = int(item["salary"]["from"])
                    salary_to = None
                else:
                    salary_from = int(item["salary"]["from"])
                    salary_to = int(item['salary']['to'])
                if not item['salary']['currency']:
                    salary_currency = None
                else:
                    salary_currency = item['salary']['currency']
            result.append({'name': item['name'], 'salary_from': salary_from, 'salary_to': salary_to,
                           'salary_currency': salary_currency, 'url': item['alternate_url'],
                           'employer_id': int(item['employer']['id'])})
        return result
