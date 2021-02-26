FROM python:3.9.1
ENV PYTHONUNBUFFERED=1
WORKDIR /usr/src/hh_ru_django
COPY requirements.txt /usr/src/hh_ru_django/
RUN pip install -r requirements.txt
COPY . /usr/src/hh_ru_django
CMD python3 parse_all_ads.py