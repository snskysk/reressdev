from grade.settings import *

DEBUG = True



DATABASES = {

       'default': {
       'ENGINE': 'django.db.backends.postgresql_psycopg2',
       'NAME': 'gradedb',
       'USER': 'shunsuke',
       'PASSWORD': 'shun0210',
       'HOST': '127.0.0.1',
       'POST': '5432'
     }
}