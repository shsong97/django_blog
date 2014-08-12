django_blog
===========

blog, poll, bookmark for django-python




# Set up PostgreSQL
============

Installation

for windows x86

1) Download "postgresql-9.3.4-3-windows.exe" file and setup

URL : http://www.stickpeople.com/projects/python/win-psycopg/


2) Download PostgreSQL and setup

URL : http://www.postgresql.org/download/

3) Edit setting.py of your project

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'blog',
        'USER': 'postgres',
        'PASSWORD':'1234',
}

# Set up for Apache Server
============



Installation

1. Set up apache ver2.2.

URL : 

1) http://httpd.apache.org/

2) http://mirror.apache-kr.org//httpd/binaries/win32/

No ssl version : httpd-2.2.25-win32-x86-no_ssl.msi


2. Set up mod wsgi for Django

1) Download "mod_wsgi-win32-ap22py27-3.3" file

URL : https://code.google.com/p/modwsgi/downloads/detail?name=mod_wsgi-win32-ap22py27-3.3.so

2) Rename mod_wsgi-win32-ap22py27-3.3.so to mod_wsgi.so

3) Copy file

Directory : C:\Program Files\Apache Software Foundation\Apache2.2\modules


4) Edit "httpd.conf" file

C:\Program Files\Apache Software Foundation\Apache2.2\conf\httpd.conf 

Add below:

# WSGI Setting for Django

LoadModule wsgi_module modules/mod_wsgi.so

WSGIScriptAlias / d:/django_blog/apache/django.wsgi

<Directory "d:/django_blog/apache">

Order deny,allow

Allow from all

</Directory>

Alias /static d:/django_blog/apache/static

<Directory "d:/django_blog/apache/static">

Order deny,allow

Allow from all

</Directory>


5) Edit "django.wsgi" file

import os

import sys

sys.path.append('d:/django_blog')

os.environ['DJANGO_SETTINGS_MODULE']='mysite.settings'

import django.core.handlers.wsgi

application=django.core.handlers.wsgi.WSGIHandler()
