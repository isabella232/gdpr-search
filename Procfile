release: DJANGO_SETTINGS_MODULE='gdpr.settings.prod' python manage.py migrate
web: DJANGO_SETTINGS_MODULE='gdpr.settings.prod' gunicorn gdpr.wsgi --log-file -
