from grade.settings import *

DEBUG = True



DATABASES = {
    'default': {
         'ENGINE': 'django.db.backends.postgresql_psycopg2',
         'NAME': 'grade',
         'USER': 'gouta',
         'PASSWORD' : 'bellona',
         'HOST' : '127.0.0.1',
         'PORT' : '5432',
     }
 }