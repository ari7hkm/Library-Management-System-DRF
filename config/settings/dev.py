from . common import *

DEBUG = True

SECRET_KEY = 'django-insecure-()6(7vh3x%$@f3@bow5l-%i_kh8m9li1x0se60ilo2(03rp*-7'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'library',
        'HOST': 'localhost', # The host
        'USER': 'root', # The User
        'PASSWORD': 'mysqlpass' # The password
    }
}