from .base import *

import django_heroku

DEBUG = False
COMPRESS_OFFLINE = True

django_heroku.settings(locals())
