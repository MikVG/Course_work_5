# Course_work_5

Программа выполняет парсинг вакансий в сайта HeadHunter по следующим работодателям:

- Сбер
- Лаборатория Касперского
- OZON
- Яндекс
- Тинькофф
- Авито
- Райффайзенбанк
- Альфа Банк
- X5 Tech
- Иннотех


Инструкция по развертыванию.
Необходимо создать базу данный vacancy
Выполнить следующие скрипты в этой БД для создания таблиц:

CREATE TABLE company (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255),
  city VARCHAR(70),
  external_id INT,
  description TEXT,
  site_url TEXT
);

CREATE TABLE vacancy (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255),
  external_id INT,
  description TEXT,
  salary_from INT,
  salary_to INT,
  url TEXT,
  employer_id INT
);