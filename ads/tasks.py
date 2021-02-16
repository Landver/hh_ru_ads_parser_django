from __future__ import absolute_import, unicode_literals

from .scrapers import parser_hh

from celery import shared_task


url = "https://hh.ru/search/vacancy?L_is_autosearch=false&area=113&clusters=true&enable_snippets=true&only_with_salary=true&order_by=publication_time&search_period=1&page=0"


@shared_task
def scrape_ads():
    parser_hh(url)
    return


@shared_task
def hello():
    print('hello')
    return
