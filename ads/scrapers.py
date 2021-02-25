import requests

from hhparser.hhru_parser import HhruParser

from .models import Ad
import time

def parser_hh(url):
    '''
        Запускает движок браузера и начинает парсить сайт hh.ru
        Активируется из под celery
    '''
    # parser = HhruParser('no-javascript')
    # for i in range(41000000, 42520047):
    #     parser.driver.get(f'https://hh.ru/vacancy/{i}')
    #     title = parser.get_title()
    #     company_name = parser.get_company_name()
    #     city = parser.get_address()
    #     salary = parser.get_salary()
    #     work_experience = parser.get_experience()
    #     type_of_employment = parser.get_type_of_employment()
    #     description = parser.get_description()
    #     if title == '':
    #         state = 'Не найдено'
    #     elif title != '' and description == '':
    #         state = 'В архиве'
    #     url = parser.get_current_url()
    #     parser.driver.get(f'https://hh.ru/vacancy/{i}')
    #     r = requests.post("http://65.21.6.232:8888/api/v1/ads/", {'title': title,
    #                                                               'company_name': company_name,
    #                                                               'city': city,
    #                                                               'salary': salary,
    #                                                               'work_experience': work_experience,
    #                                                               'employment_type': type_of_employment,
    #                                                               'description': description,
    #                                                               'vacancy_url': url,
    #                                                               'phone': "",
    #                                                               'email': "",
    #                                                               'state': state})
    #     print(r.status_code)

    parser = HhruParser('no-javascript')
    parser.driver.get(url)
    print(parser.driver.current_url)
    for page in range(1, 40):  # число 40 это максимальное число страниц в поиске hh.ru
        ads = parser.get_list_of_ads()
        for ad in ads:
            parser.get_detail_page(ad)
            title = parser.get_title()
            company_name = parser.get_company_name()
            city = parser.get_address()
            salary = parser.get_salary()
            work_experience = parser.get_experience()
            type_of_employment = parser.get_type_of_employment()
            description = parser.get_description()
            url = parser.get_current_url()
            parser.close_detail_page()
            r = requests.post("http://135.181.195.100:8888/api/v1/ads/", {'title': title,
                                                                          'company_name': company_name,
                                                                          'city': city,
                                                                          'salary': salary,
                                                                          'work_experience': work_experience,
                                                                          'employment_type': type_of_employment,
                                                                          'description': description,
                                                                          'vacancy_url': url,
                                                                          'phone': "",
                                                                          'email': ""})
            print(r.status_code)
        parser.next_page()


def scrape_contacts():
    ads = Ad.objects.filter(parsed=False)
    print(ads)
    parser = HhruParser()
    for ad in ads:
        parser.driver.get(ad.vacancy_url)
        parser.show_contacts()
        phone = parser.get_phone()
        email = parser.get_email()
        r = requests.patch("http://135.181.195.100:8888/api/v1/ads/{}/".format(str(ad.id)), {'phone': phone, 'email': email, 'parsed': True})
        print(r.status_code)
        if r.status_code == 200:
            print('Добавлено')
        elif r.status_code == 404:
            print('Страница не найдена')
        elif r.status_code == 500:
            print('Доступ запрещен')
