from __future__ import absolute_import, unicode_literals

from .scrapers import parser_hh

from celery import shared_task


@shared_task
def scrape_ads():
    parser_hh()
    return
