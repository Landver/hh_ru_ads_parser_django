Create config.env file in the root of project
SET environment variables in config.env

SECRET_KEY=(your secret key for django project)
DJANGO_DEBUG=(True or False)
POSTGRES_DB=(name of your database for postgres, or use your own settings if other db)
POSTGRES_USER=(username of your database for postgres, or use your own settings if other db)
POSTGRES_PASSWORD=(password of your database for postgres, or use your own settings if other db)
CELERY_BROKER=redis://redis:6379/0
CELERY_BACKEND=redis://redis:6379/0
SE_EVENT_BUS_HOST=selenium-hub
SE_EVENT_BUS_PUBLISH_PORT=4442
SE_EVENT_BUS_SUBSCRIBE_PORT=4443
