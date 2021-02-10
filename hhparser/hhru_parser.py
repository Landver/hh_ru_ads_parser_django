from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException


PATH = "C:/Program Files (x86)/chromedriver.exe"


class HhruParser:
    '''Скрапер для hh.ru'''
    def __init__(self, **kwargs):
        '''Инициализируем драйвер браузера'''
        if kwargs['browser'] == 'Chrome':
            self.driver = webdriver.Chrome(executable_path=kwargs['path_to_driver'])
            self.driver.get(kwargs['url'])
        elif kwargs['browser'] == 'Firefox':
            self.driver = webdriver.Firefox(executable_path=kwargs['path_to_driver'])
            self.driver.get(kwargs['url'])

    def get_page_blocks(self):
        '''Получаем блок со стрницами в футере сайта hh.ru'''
        page_blocks = self.driver.find_elements_by_class_name("pager-item-not-in-short-range")
        return page_blocks

    def get_num_of_pages(self, page_block):
        '''Получаем количество страниц с объявлениями'''
        page_block = page_block[-1]
        pages = page_block.find_elements_by_class_name("bloko-button")[0].text
        return pages

    def next_page(self, page_block):
        '''Переходит на следующую страницу'''
        self.driver.find_element(By.XPATH, '//a[text()="дальше"]').click()

    def get_list_of_ads(self):
        '''Получаем список объявлений на одной странице'''
        ads = self.driver.find_elements_by_class_name("vacancy-serp-item")
        return ads

    def get_ad(self, list_of_ads, index_of_ad):
        '''Получаем одно объявление из списка страниц'''
        return list_of_ads[index_of_ad]

    def get_title(self, ad):
        '''Получаем название объявления'''
        name = ad.find_elements_by_class_name("g-user-content")[0].text
        return name

    def get_city(self, ad):
        return ad.find_element_by_css_selector('[data-qa="vacancy-serp__vacancy-address"]').text.split(', ')[0]

    def get_company_name(self, ad):
        return ad.find_element_by_class_name("vacancy-serp-item__meta-info-company").text

    def get_description(self, ad):
        '''Получаем описание
           Работает только если мы перешли к деталям объявления (либо при помощи ссылки либо при помощи метода go_ad_detail)
        '''
        ad.find_elements_by_class_name("g-user-content")[0].click()
        self.driver.switch_to.window(self.driver.window_handles[1])
        description = self.driver.find_element_by_class_name("vacancy-description").text
        description_list = description.split('\n')
        work_experience = description_list[0].split(': ')
        working_day = description_list[1].split(', ')
        if "\nКлючевые навыки" in description:
            description = '\n'.join(description_list[2:]).split("\nКлючевые навыки")[0]
        else:
            description = '\n'.join(description_list[2:]).split("\nПоказать на большой карте")[0]
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])
        return {'work_experience': work_experience[1], 'working_day': working_day, 'description': description}

    def get_phone(self, ad):
        '''Получаем номер телефона'''
        if ad.find_elements_by_class_name("vacancy-serp-item__control"):
            phone = ad.find_elements_by_class_name("vacancy-serp-item__control")[0]
            phone.click()
            try:
                number = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "vacancy-contacts__phone-text"))
                )
                return number.text
            except:
                return "Номер отсутствует"
            phone.click()
        else:
            return "Номер отсутствует"

    def get_first_page(self, ad):
        '''Переходит на первую страницу'''
        try:
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-qa='first-page']")))
        except NoSuchElementException:
            print("Нет кнопки в начало")

    def get_salary(self, ad):
        '''Получаем зарплату на вакансии
        '''
        try:
            salary = ad.find_element_by_css_selector("[data-qa='vacancy-serp__vacancy-compensation']").text
        except NoSuchElementException:
            salary = None
        if salary is None:
            return salary
        elif '-' in salary:
            '''Преобразуем зарплату в том случае если она дается в диапазоне'''
            salary = salary.split('-')
            min_salary = int(''.join(salary[0].split(' ')))
            max_salary = int(''.join(list(filter(lambda x: x if x.isdigit() else None, salary[1].split(' ')))))
            return min_salary, max_salary
        else:
            '''Преобразуем зарплату в другом случае'''
            return int(''.join(list(filter(lambda x: x if x.isdigit() else None, salary.split(' ')))))


parser = HhruParser(path_to_driver=PATH, browser='Chrome', url="https://hh.ru/search/vacancy?order_by=publication_time&clusters=true&area=113&enable_snippets=true")
ads = parser.get_list_of_ads()
ad = parser.get_ad(ads, 0)
print(parser.get_title(ad))
print(parser.get_company_name(ad))
print(parser.get_city(ad))
print(parser.get_description(ad))
print(parser.get_salary(ad))
print(parser.get_phone(ad))
