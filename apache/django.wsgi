import os
import sys
sys.path.append('d:/django_blog')
os.environ['DJANGO_SETTINGS_MODULE']='mysite.settings'

import django.core.handlers.wsgi
application=django.core.handlers.wsgi.WSGIHandler()