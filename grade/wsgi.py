"""
WSGI config for grade project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os
import sys

sys.path.append("/path/to/project/grade")
sys.path.append("/path/to/project/grade/grade_die")


from django.core.wsgi import get_wsgi_application
from dj_static import Cling


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'grade.settings')

application = Cling(get_wsgi_application())


#application = get_wsgi_application()

#from whitenoise.django import DjangoWhiteNoise
#application = DjangoWhiteNoise(application)
