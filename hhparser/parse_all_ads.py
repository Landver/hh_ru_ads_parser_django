import requests
from hhru_parser import HhruParser
from ads.models import Ad

# Этот скрипт нужно запустить на друг
def scrape_contacts():
    ads = Ad.objects.filter(parsed=False)
    print(ads)
    parser = HhruParser()
    for ad in ads:
        parser.driver.get(ad.vacancy_url)
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