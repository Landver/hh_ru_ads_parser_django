import requests
from hhru_parser import HhruParser
from ads.models import Ad
import os

# Этот скрипт нужно запустить на друг
def scrape_contacts():
    ads = Ad.objects.filter(parsed=False)
    print(ads)
    parser = HhruParser()
    for ad in ads:
        parser.driver.get(ad.vacancy_url)
        phone = parser.get_phone()
        email = parser.get_email()
        ip = os.getenv('ip_address_server')
        r = requests.patch("http://{}:8890/api/v1/ads/{}/".format(ip, str(ad.id)), {'phone': phone, 'email': email, 'parsed': True})
        print(r.status_code)
        if r.status_code == 200:
            print('Добавлено')
        elif r.status_code == 404:
            print('Страница не найдена')
        elif r.status_code == 500:
            print('Доступ запрещен')