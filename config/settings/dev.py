import environ
from . common import *


env = environ.Env()
environ.Env.read_env()


DEBUG = True

SECRET_KEY = 'django-insecure-()6(7vh3x%$@f3@bow5l-%i_kh8m9li1x0se60ilo2(03rp*-7'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': env('DATABASE_NAME'),
        'HOST': env('DATABASE_HOST'), # The host
        'USER': env('DATABASE_USER'), # The User
        'PASSWORD': env('DATABASE_PASSWORD') # The password
    }
}