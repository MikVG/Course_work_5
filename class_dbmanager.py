import psycopg2
import os


class DBManager:
    """
    Класс для работы с БД6 выполняет запросы для поиска информации и выводит их на экран
    """

    localhost = os.getenv('LOCALHOST')
    database = os.getenv('DATABASE')
    user = os.getenv('USR')
    password = os.getenv('PASSWORD')

    def __init__(self):
        """
        Функция для инициации экземпляра класса
        """
        pass

    def get_companies_and_vacancies_count(self):
        """
        Выводит список всех компаний и количество вакансий у каждой компании
        :return:
        """
        conn = psycopg2.connect(host=self.localhost, database=self.database, user=self.user, password=self.password)
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT cm.name, count(vc.name) "
                                "FROM company as cm "
                                "JOIN vacancy as vc "
                                "ON cm.external_id = vc.employer_id "
                                "GROUP BY cm.name")
                    companies_and_vacancies = cur.fetchall()
                    for row in companies_and_vacancies:
                        print(f'Компания: {row[0]}, '
                              f'Количество вакансий: {row[1]}')
        finally:
            conn.close()

    def get_all_vacancies(self):
        """
        Выводит список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию
        :return:
        """
        conn = psycopg2.connect(host=self.localhost, database=self.database, user=self.user, password=self.password)
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT cm.name, vc.name, salary_from, salary_to, url "
                                "FROM vacancy as vc "
                                "JOIN company as cm "
                                "ON vc.employer_id = cm.external_id")
                    all_vacancies = cur.fetchall()
                    for row in all_vacancies:
                        print(f'Работодатель: {row[0]}, '
                              f'Вакансия: {row[1]}, '
                              f'Зарплата от: {row[2]}, '
                              f'Зарплата до: {row[3]}, '
                              f'Ссылка на вакансию: {row[4]}')
        finally:
            conn.close()

    def get_avg_salary(self):
        """
        Выводит среднюю зарплату по вакансиям
        :return:
        """
        conn = psycopg2.connect(host=self.localhost, database=self.database, user=self.user, password=self.password)
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT round(avg(salary_from + salary_to)) "
                                "FROM vacancy")
                    avg_salary = cur.fetchone()
                    print(f'Средняя зарплата - {avg_salary[0]}')
        finally:
            conn.close()

    def get_vacancies_with_higher_salary(self):
        """
        Выводит список всех вакансий, у которых зарплата выше средней по всем вакансиям
        :return:
        """
        conn = psycopg2.connect(host=self.localhost, database=self.database, user=self.user, password=self.password)
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT name "
                                "FROM vacancy WHERE (salary_from + salary_to) > "
                                "(SELECT avg(salary_from + salary_to) FROM vacancy)")
                    vacancies_with_higher_salary = cur.fetchall()
                    for row in vacancies_with_higher_salary:
                        print(f'Вакансия: {row[0]}')
        finally:
            conn.close()

    def get_vacancies_with_keyword(self, keyword):
        """
        Выводит список всех вакансий, в названии которых содержатся переданные в метод слова
        :return:
        """
        conn = psycopg2.connect(host=self.localhost, database=self.database, user=self.user, password=self.password)
        keyword = f"%{keyword}%"
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT name "
                                "FROM vacancy "
                                "WHERE name LIKE %s", (keyword,))
                    vacancies_with_keyword = cur.fetchall()
                    for row in vacancies_with_keyword:
                        print(f'Вакансия: {row[0]}')
        finally:
            conn.close()
