from utils import company_parser, vacancy_parser, delete_database, create_database,  create_table, write_to_table
from class_dbmanager import DBManager


def start_program():
    """
    Стартовая функция работы программы. Выполняет создание БД, таблиц БД, парсинг компаний и вакансий с HeadHunter
    :return:
    """
    create_database()

    create_table()

    company_list = company_parser()
    write_to_table(company_list, 'company')

    vacancy_list = vacancy_parser()
    write_to_table(vacancy_list, 'vacancy')


def exit():
    """
    Функция для выполнения выхода из программы, выполняет также удаление БД перед выходом из программы
    :return:
    """
    delete_database()
    print("Программа завершила работу!")


def user_return():
    """
    Функция для возврата в главное меню или выхода из программы
    :return:
    """
    user_return = input("""\nВернуться в главное меню?
    1 - Да
    2 - Выйти из программы
    """)
    if user_return == '1':
        main()
    else:
        exit()

def main():
    """
    Функция навигации по пользовательскому меню
    :return:
    """
    print("""Программа для загрузки информации по вакансиям с сайта HeadHunter по компаниям:
Сбер, Лаборатория Касперского, OZON, Яндекс, Тинькофф, Авито, Райффайзенбанк, Альфа Банк, X5 Tech, Иннотех\n""")

    db_manager = DBManager()

    print("""По списку вакансий можно получить следующую информацию:
    1 - получить список всех компаний и количество вакансий у каждой компании
    2 - получить список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию
    3 - получить среднюю зарплату по вакансиям
    4 - получить список всех вакансий, у которых зарплата выше средней по всем вакансиям
    5 - получить список всех вакансий, в названии которых содержатся переданные в метод слова
    6 - выйти из программы
    """)

    user_choise = input("Какую информацию вы хотите получить? ")

    if user_choise == '1':
        db_manager.get_companies_and_vacancies_count()
        user_return()
    elif user_choise == '2':
        db_manager.get_all_vacancies()
        user_return()
    elif user_choise == '3':
        db_manager.get_avg_salary()
        user_return()
    elif user_choise == '4':
        db_manager.get_vacancies_with_higher_salary()
        user_return()
    elif user_choise == '5':
        keyword = input("Введите слово для поиска вакансии: ")
        db_manager.get_vacancies_with_keyword(keyword)
        user_return()
    else:
        exit()


if __name__ == '__main__':
    start_program()
    main()
