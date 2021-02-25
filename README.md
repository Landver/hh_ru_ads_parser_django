# Docker.io needs to be installed 

# Create config.env file in the root of project and set environment variables in config.env
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

### To run, open shell in the root of your project, and write docker-compose up
