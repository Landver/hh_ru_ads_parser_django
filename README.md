# Docker.io нужен для работы сайта
# Также создайте папку logs в папке hh_ru_django , внутри logs создайте файл debug.log
# создайте файл config.env в корне проекта и поместите туда данные переменные 
SECRET_KEY=**"Your secret key for django project"**<br>
DJANGO_DEBUG=**"True or False"**<br>
POSTGRES_DB=**"name of your database for postgres, or use your own settings if other db"**<br>
POSTGRES_USER=**"username of your database for postgres, or use your own settings if other db"**<br>
POSTGRES_PASSWORD=**"password of your database for postgres, or use your own settings if other db"**<br>
CELERY_BROKER=**redis://redis:6379/0**<br>
CELERY_BACKEND=**redis://redis:6379/0**<br>
SE_EVENT_BUS_HOST=**selenium-hub**<br>
SE_EVENT_BUS_PUBLISH_PORT=**4442**<br>
SE_EVENT_BUS_SUBSCRIBE_PORT=**4443**<br>
ALLOWED_HOST= **"your hostname"**

### Для запуска откройте командную строку в корне проекта и пропишите docker-compose up
В папке hhparser лежит сам парсер + 2 скрипта для отправки данных к серверу,
один занимается тем что добавляет контакты к тем объявлениям что есть в базе,
другой тем что просматривает последние 40 страниц новых объявлений, 
скрипты желательно использовать на разных машинах , и запускать параллельно.