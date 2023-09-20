from src.DBManager import DBManager

# Инициализируем класс менеджера баз данных
dbm = DBManager()

# Создаем таблицы по списку идентификаторов работодателей
dbm.create_db([1740, 3529, 84585, 3127, 4934, 3776, 4496, 78638, 1455, 1809605])

# Cписок компаний и количество вакансий
dbm.get_companies_and_vacancies_count()

# Список всех вакансий
dbm.get_all_vacancies()

# Средняя зарплата
dbm.get_avg_salary()

# Зарплата выше средней
dbm.get_vacancies_with_higher_salary()

# Вакансии по ключевому слову
dbm.get_vacancies_with_keyword('Аналитик')
