from dotenv import load_dotenv
import os
import requests
import re
import psycopg2
from psycopg2 import extensions

load_dotenv()

employers_list = [3529, 1057, 2180, 1740, 78638, 84585, 4023, 80, 9352463, 4649269]
company_list = []
vacancy_list = []


def company_parser():
    """
    Функция для получения информации по работодателям с сайта HeadHunter
    :return: company_list
    """

    for emp in employers_list:
        URL = f'https://api.hh.ru/employers/{emp}'
        responce = requests.get(URL)

        data = responce.json()
        data['description'] = re.sub("<p>|</p>|<em>|<br />|<strong>|</strong>|"
                                     "</em>|amp;|</li>|<li>|&mdash;|&nbsp;|&laquo;|"
                                     "&raquo;|<ul>|</ul>|&ndash;|&middot; ", "", data['description'])

        company_list.append((data['name'], data['area']['name'], data['id'], data['description'], data['site_url']))

    return company_list


def vacancy_parser():
    """
    Функция для получения информации по вакансиям работодателей с сайта HeadHunter
    :return: vacancy_list
    """
    for emp_id in employers_list:
        url = f'https://api.hh.ru/vacancies?employer_id={emp_id}'
        res = requests.get(url)
        data = res.json()['items']

        for item in data:
            name = item['name']
            id_vacancy = item['id']
            responsibility = item['snippet']['responsibility']
            if item['salary'] is None:
                salary_from = 0
                salary_to = 0
            else:
                if item['salary']['from'] is None:
                    salary_from = 0
                else:
                    salary_from = item['salary']['from']
                if item['salary']['to'] is None:
                    salary_to = 0
                else:
                    salary_to = item['salary']['to']
            alternate_url = item['alternate_url']
            employer_id = item['employer']['id']

            vacancy_list.append((name, id_vacancy, responsibility, salary_from, salary_to, alternate_url, employer_id))

    return vacancy_list


def create_database():
    """
    Функция создания БД
    :return:
    """
    localhost = os.getenv('LOCALHOST')
    user = os.getenv('USR')
    password = os.getenv('PASSWORD')

    auto_commit = extensions.ISOLATION_LEVEL_AUTOCOMMIT
    conn = psycopg2.connect(host=localhost, database='postgres', user=user, password=password)
    conn.set_isolation_level(auto_commit)
    cur = conn.cursor()
    cur.execute("CREATE DATABASE vacancy")
    conn.close()


def delete_database():
    """
    Функция удаления БД
    :return:
    """
    localhost = os.getenv('LOCALHOST')
    user = os.getenv('USR')
    password = os.getenv('PASSWORD')

    auto_commit = extensions.ISOLATION_LEVEL_AUTOCOMMIT
    conn = psycopg2.connect(host=localhost, database='postgres', user=user, password=password)
    conn.set_isolation_level(auto_commit)
    cur = conn.cursor()
    cur.execute("DROP DATABASE vacancy")
    conn.close()


def create_table():
    """
    Функция для создания таблиц company и vacancy. Если таблицы существуют, то они не создаются
    :return:
    """

    localhost = os.getenv('LOCALHOST')
    database = os.getenv('DATABASE')
    user = os.getenv('USR')
    password = os.getenv('PASSWORD')

    conn = psycopg2.connect(host=localhost, database=database, user=user, password=password)
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("CREATE TABLE IF NOT EXISTS company "
                            "(id SERIAL PRIMARY KEY,"
                            "name VARCHAR(255),"
                            "city VARCHAR(70),"
                            "external_id INT,"
                            "description TEXT,"
                            "site_url TEXT)")

                cur.execute("CREATE TABLE IF NOT EXISTS vacancy ("
                            "id SERIAL PRIMARY KEY,"
                            "name VARCHAR(255),"
                            "external_id INT,"
                            "description TEXT,"
                            "salary_from INT,"
                            "salary_to INT,"
                            "url TEXT,"
                            "employer_id INT)")
    finally:
        conn.close()


def write_to_table(lst, table_name):
    """
    Функция для заполнения данных в таблицы работодателей (company) и вакансий (vacancy) в БД PostgreSQL
    :param lst:
    :param table_name:
    :return:
    """

    localhost = os.getenv('LOCALHOST')
    database = os.getenv('DATABASE')
    user = os.getenv('USR')
    password = os.getenv('PASSWORD')

    conn = psycopg2.connect(host=localhost, database=database, user=user, password=password)
    try:
        with conn:
            with conn.cursor() as cur:
                for item in lst:
                    if table_name == 'company':
                        cur.execute("INSERT INTO company (name, city, external_id, description, site_url)"
                                    " VALUES (%s, %s, %s, %s, %s)", item)
                    elif table_name == 'vacancy':
                        cur.execute("INSERT INTO vacancy "
                                    "(name, external_id, description, salary_from, salary_to, url, employer_id)"
                                    " VALUES (%s, %s, %s, %s, %s, %s, %s)", item)
    finally:
        conn.close()
