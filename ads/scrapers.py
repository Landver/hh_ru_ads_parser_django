import requests

from hhparser.hhru_parser import HhruParser

from .models import Ad


def parser_hh(url):
    '''
        Запускает движок браузера и начинает парсить сайт hh.ru
        Активируется из под celery
    '''
    parser = HhruParser('no-javascript')
    parser.driver.get(url)
    for page in range(1, 40):  # число 40 это максимальное число страниц в поиске hh.ru
        ads = parser.get_list_of_ads()
        for ad in ads:
            title = parser.get_title(ad)
            company_name = parser.get_company_name(ad)
            city = parser.get_city(ad)
            salary = parser.get_salary(ad)
            parser.get_detail_page(ad)
            work_experience = parser.get_experience()
            type_of_employment = parser.get_type_of_employment()
            description = parser.get_description()
            url = parser.get_current_url()
            parser.close_detail_page()
            r = requests.post("http://65.21.6.232:8888/api/v1/ads/", {'title': title,
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
    ads = Ad.objects.all()
    parser = HhruParser()
    for ad in ads:
        if ad.parsed is False:
            parser.driver.get(ad.vacancy_url)
            parser.show_contacts()
            phone = parser.get_phone()
            email = parser.get_email()
            r = requests.patch("http://65.21.6.232:8888/api/v1/ads/{}".format(str(ad.id)), {'phone': phone, 'email': email})
