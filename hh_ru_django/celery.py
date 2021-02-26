from __future__ import absolute_import, unicode_literals

import os

from celery.schedules import crontab

from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hh_ru_django.settings')


app = Celery('hh_ru_django')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings', namespace="CELERY")

app.conf.timezone = 'Europe/Moscow'


app.conf.beat_schedule = {
    'parser_hh': {
        'task': 'ads.tasks.scrape_ads',
        'schedule': crontab(day_of_month='26'),
        'args': (),
    }
}

app.autodiscover_tasks()
