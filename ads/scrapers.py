import requests

from hhparser.hhru_parser import HhruParser
from .models import Ad


def parser_hh(url):
    '''
        Запускает движок браузера и начинает парсить сайт hh.ru
        Активируется из под celery
    '''
    print('hello')
    ads = Ad.objects.all()
    print('hello')
    min_ad_num = ads.order_by('created_date').reverse()[0]
    min_ad_num = int(min_ad_num.vacancy_url.split('/')[-1])
    max_ad_num = max([int(i.vacancy_url.split('/')[-1]) for i in ads])
    parser = HhruParser('no-javascript')
    print('hello')
# Скрипт который нужно запустить для получения данных в заданом диапазоне
    for i in range(min_ad_num, max_ad_num):
        url = f'https://hh.ru/vacancy/{i}'
        if ads.filter(vacancy_url=url):
            print(f"{url} в базе")
            continue
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
        r = requests.post("http://135.181.195.100:80/api/v1/ads/", {'title': title,
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