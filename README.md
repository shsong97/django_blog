django_blog
===========

blog, poll, bookmark for django-python




Set up PostgreSQL
============

Installation for windows x86

1) Download "postgresql-9.3.4-3-windows.exe" file and setup

URL : http://www.stickpeople.com/projects/python/win-psycopg/

2) Download PostgreSQL and setup

URL : http://www.postgresql.org/download/

3) Edit setting.py of your project
<pre>
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'blog',
        'USER': 'postgres',
        'PASSWORD':'1234',
}
</pre>

Set up for Apache Server
============

Installation

1. Set up apache ver2.2.<br />
Download no ssl version : httpd-2.2.25-win32-x86-no_ssl.msi<br />
URL : <br />
1) http://httpd.apache.org/ or <br /> 
2) http://mirror.apache-kr.org//httpd/binaries/win32/ <br />

2. Set up mod wsgi for Django<br />
1) Download "mod_wsgi-win32-ap22py27-3.3" file<br />
URL : https://code.google.com/p/modwsgi/downloads/detail?name=mod_wsgi-win32-ap22py27-3.3.so<br />
2) Rename mod_wsgi-win32-ap22py27-3.3.so to mod_wsgi.so<br />
3) Copy file<br />
Directory : C:\Program Files\Apache Software Foundation\Apache2.2\modules<br />
4) Edit "httpd.conf" file<br />
Directory : C:\Program Files\Apache Software Foundation\Apache2.2\conf\httpd.conf <br />
Add below:<br />
<pre>
LoadModule wsgi_module modules/mod_wsgi.so
WSGIScriptAlias / d:/django_blog/apache/django.wsgi
&lt;Directory "d:/django_blog/apache">
Order deny,allow
Allow from all
&lt;/Directory>
Alias /static d:/django_blog/apache/static
&lt;Directory "d:/django_blog/apache/static">
Order deny,allow
Allow from all
&lt;/Directory>
</pre>

5) Edit "django.wsgi" file
<pre>
import os
import sys
sys.path.append('d:/django_blog')
os.environ['DJANGO_SETTINGS_MODULE']='mysite.settings'
import django.core.handlers.wsgi
application=django.core.handlers.wsgi.WSGIHandler()
</pre>
