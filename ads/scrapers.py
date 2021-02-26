import requests

from hhparser.hhru_parser import HhruParser
from .models import Ad


def parser_hh(url):
    '''
        Запускает движок браузера и начинает парсить сайт hh.ru
        Активируется из под celery
    '''
    ads = Ad.objects.all()
    max_ad_num = max([int(i.vacancy_url.split('/')[-1]) for i in ads])
    parser = HhruParser('no-javascript')
# Скрипт который нужно запустить для получения данных в заданом диапазоне
    for i in range(41000000, max_ad_num):
        url = f'https://hh.ru/vacancy/{i}'
        if ads.filter(vacancy_url=url):
            print("Объявление уже естьв базе")
            continue
        parser.driver.get(url)
        try:
            parser.driver.find_element_by_class_name("attention_bad")
            continue
        except:
            title = parser.get_title()
            company_name = parser.get_company_name()
            city = parser.get_address()
            salary = parser.get_salary()
            work_experience = parser.get_experience()
            type_of_employment = parser.get_type_of_employment()
            description = parser.get_description()
            if title == '':
                state = 'Не найдено'
            elif title != '' and description == '':
                state = 'В архиве'
            r = requests.post("http://135.181.195.100:8888/api/v1/ads/", {'title': title,
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
    



