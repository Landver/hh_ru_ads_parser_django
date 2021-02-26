import requests

from hhru_parser import HhruParser
from ads.models import Ad
url = "https://rostov.hh.ru/search/vacancy?clusters=true&enable_snippets=true&only_with_salary=true&order_by=publication_time&search_period=1&L_save_area=true&area=113&from=cluster_area&showClusters=true"

parser = HhruParser()
base_ads = Ad.objects.all()
parser.driver.get(url)
print(parser.driver.current_url)
for page in range(1, 40):  # число 40 это максимальное число страниц в поиске hh.ru
    # Получаем все объявления
    ads = parser.get_list_of_ads()
    # Проходимся по каждому объявлению
    for ad in ads:
        parser.get_detail_page(ad)
        url = parser.get_current_url()
        if base_ads.filter(vacancy_url=url):
            print('Объявление уже добавлено')
            parser.close_detail_page()
            continue
        parser.show_contacts()
        phone = parser.get_phone()
        email = parser.get_email()
        # Достаем основные данные из объявления
        title = parser.get_title()
        company_name = parser.get_company_name()
        city = parser.get_address()
        salary = parser.get_salary()
        work_experience = parser.get_experience()
        type_of_employment = parser.get_type_of_employment()
        description = parser.get_description()
        parser.close_detail_page()

        # отправляем данные на сервер
        r = requests.post("http://135.181.195.100:8888/api/v1/ads/", {'title': title,
                                                                      'company_name': company_name,
                                                                      'city': city,
                                                                      'salary': salary,
                                                                      'work_experience': work_experience,
                                                                      'employment_type': type_of_employment,
                                                                      'description': description,
                                                                      'vacancy_url': url,
                                                                      'phone': phone,
                                                                      'email': email})
        print(r.status_code)
    parser.next_page()
