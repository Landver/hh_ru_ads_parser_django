import time
import requests
# from pyvirtualdisplay import Display


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class HhruParser:
    '''Скрапер для hh.ru'''
    def __init__(self, **kwargs):
        '''Инициализируем драйвер браузера'''
        caps = DesiredCapabilities.CHROME
        self.driver = webdriver.Remote(
            command_executor='http://65.21.6.232:4444/wd/hub',
            desired_capabilities=caps)

    def get_page_blocks(self):
        '''Получаем блок со стрницами в футере сайта hh.ru'''
        page_blocks = self.driver.find_elements_by_class_name("pager-item-not-in-short-range")
        return page_blocks

    def get_num_of_pages(self, page_block):
        '''Получаем количество страниц с объявлениями'''
        page_block = page_block[-1]
        pages = page_block.find_elements_by_class_name("bloko-button")[0].text
        return pages

    def next_page(self):
        '''Переходит на следующую страницу'''
        next_page = self.driver.find_element_by_css_selector('[data-qa="pager-next"]')
        ActionChains(self.driver).click(next_page).perform()

    def get_list_of_ads(self):
        '''Получаем список объявлений на одной странице'''
        ads = self.driver.find_elements_by_class_name("vacancy-serp-item")
        return ads

    def get_ad(self, list_of_ads, index_of_ad):
        '''Получаем одно объявление из списка страниц'''
        return list_of_ads[index_of_ad]

    def get_title(self, ad):
        '''Получаем название объявления'''
        name = WebDriverWait(ad, 2).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-qa="vacancy-serp__vacancy-title"]'))
        ).text
        return name

    def get_city(self, ad):
        return ad.find_element_by_css_selector('[data-qa="vacancy-serp__vacancy-address"]').text.split(', ')[0]

    def get_company_name(self, ad):
        return ad.find_element_by_class_name("vacancy-serp-item__meta-info-company").text

    def get_detail_page(self, ad):
        detail = ad.find_element_by_css_selector('[data-qa="vacancy-serp__vacancy-title"]')
        ActionChains(self.driver).click(detail).perform()
        self.driver.switch_to.window(self.driver.window_handles[1])

    def close_detail_page(self):
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])

    def get_experience(self):
        '''Работает только после получения детальной страницы'''
        try:
            return self.driver.find_element_by_css_selector('[data-qa="vacancy-experience"]').text
        except:
            return ""

    def get_type_of_employment(self):
        try:
            return self.driver.find_element_by_css_selector('[data-qa="vacancy-view-employment-mode"]').text
        except:
            return ""

    def get_description(self):
        try:
            return self.driver.find_element_by_css_selector('[data-qa="vacancy-description"]').text
        except:
            return ""
    def get_phone(self):
        '''Получаем номер телефона'''
        try:
            phone = self.driver.find_element_by_css_selector('[data-qa="vacancy-contacts__phone"]').text
            phone = phone.split(',')[0]
            return phone
        except:
            return ""

    def get_email(self):
        try:
            return self.driver.find_element_by_css_selector('[data-qa="vacancy-contacts__email"]').text
        except:
            return ""

    def get_first_page(self, ad):
        '''Переходит на первую страницу'''
        try:
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-qa='first-page']")))
        except NoSuchElementException:
            print("Нет кнопки в начало")

    def show_contacts(self):
        try:
            contacts = WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, '[data-qa="show-employer-contacts"]')))
            ActionChains(self.driver).click(contacts).perform()
        except:
            print('Нет данных о контактах')
        time.sleep(0.2)

    def get_salary(self, ad):
        '''Получаем зарплату на вакансии
        '''
        try:
            salary = ad.find_element_by_css_selector("[data-qa='vacancy-serp__vacancy-compensation']").text
        except:
            salary = None
        if salary is None:
            return salary
        elif '-' in salary:
            '''Преобразуем зарплату в том случае если она дается в диапазоне'''
            salary = salary.split('-')
            min_salary = int(''.join(salary[0].split(' ')))
            return min_salary
        else:
            '''Преобразуем зарплату в другом случае'''
            return int(''.join(list(filter(lambda x: x if x.isdigit() else None, salary.split(' ')))))
