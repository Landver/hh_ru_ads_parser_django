import requests
import os

from hhparser.hhru_parser import HhruParser

from .models import Ad


def parser_hh():
    '''
        Запускает движок браузера и начинает парсить сайт hh.ru
        Активируется из под celery
    '''
    parser = HhruParser()
    list_of_errors = ["tmpl_hh_form", "attention_bad", "error__content"]
    ad = Ad.objects.all().latest()
    min_ad = int(ad.vacancy_url.split('/')[-1])
    ip = os.getenv('ip_address_server')
    # Скрипт который нужно запустить для получения данных в заданом диапазоне
    for i in range(min_ad, 60000000):
        url = f'https://hh.ru/vacancy/{i}'
        if Ad.objects.filter(vacancy_url=url).first():
            continue
        parser.driver.get(url)
        print(url)
        has_errors = []
        for i in list_of_errors:
            try:
                error = parser.driver.find_element_by_class_name(i)
                has_errors.append(error)
            except:
                pass
        if not all(i == '' for i in has_errors) or not parser.driver.current_url.startswith("https://hh.ru"):
            continue
        # Пакуем данные внутрь для отправления на базу
        (title, company_name, city,
         salary, work_experience,
         type_of_employment, description, ) = (parser.get_title(), parser.get_company_name(),
                                               parser.get_address(), parser.get_salary(),
                                               parser.get_experience(), parser.get_type_of_employment(),
                                               parser.get_description())
        print(title)
        parser.show_contacts()
        email, phone = parser.get_email(), parser.get_phone()
        if title == '':
            state = 'Не найдено'
        elif title != '' and description == '':
            state = 'В архиве'
        else:
            state = 'normal'
        
        requests.post(f"http://{ip}:8890/api/v1/ads/",
                          {'title': title, 'company_name': company_name,
                           'city': city, 'salary': salary, 'work_experience': work_experience,
                           'employment_type': type_of_employment, 'description': description,
                           'vacancy_url': url, 'phone': phone, 'email': email, 'state': state})
