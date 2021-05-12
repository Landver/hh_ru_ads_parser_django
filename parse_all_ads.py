import requests
from hhparser.hhru_parser import HhruParser
import os

# Этот скрипт нужно запустить на друг
def parser_hh():
    '''
        Запускает движок браузера и начинает парсить сайт hh.ru
        Активируется из под celery
    '''
    parser = HhruParser('no-javascript')
# Скрипт который нужно запустить для получения данных в заданом диапазоне
    for i in range(42631466, 42651466):
        url = f'https://hh.ru/vacancy/{i}'
        parser.driver.get(url)
        # Есть страница в которых требуется авторизация, их мы пропускаем
        try:
            attention = parser.driver.find_element_by_class_name("attention_bad")
        except:
            attention = ''
        if attention:
            continue
        # Проверка на не найденную страницу
        try:
            not_found = parser.driver.find_element_by_class_name("error__content")
        except:
            not_found = ''
        if not_found:
            continue
        title = parser.get_title()
        company_name = parser.get_company_name()
        city = parser.get_address()
        salary = parser.get_salary()
        work_experience = parser.get_experience()
        type_of_employment = parser.get_type_of_employment()
        description = parser.get_description()
        # print(title, company_name, city, salary, work_experience, type_of_employment, description)
        if title == '':
            state = 'Не найдено'
        elif title != '' and description == '':
            state = 'В архиве'
        else:
            state = 'normal'
        ip = os.getenv('ip_address_server')
        r = requests.post(f"http://{ip}:8890/api/v1/ads/", {'title': title,
                                                                    'company_name': company_name,
                                                                    'city': city,
                                                                    'salary': salary,
                                                                    'work_experience': work_experience,
                                                                    'employment_type': type_of_employment,
                                                                    'description': description,
                                                                    'vacancy_url': url,
                                                                    'phone': '',
                                                                    'email': '',
                                                                    'state': state})
        print(r.status_code)


parser_hh()
