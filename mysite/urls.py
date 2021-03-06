from django.conf.urls import include, url
from django.contrib import admin
from mysite import views
import user_manager
 
admin.autodiscover()

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^blog/', include('blog.urls',namespace="blog")),
    url(r'^polls/', include('polls.urls',namespace="polls")),
    url(r'^user/', include('user_manager.urls',namespace="user_manager")),
    url(r'^contact/', user_manager.views.contact, name='contact'),
    url(r'i18n/',include('django.conf.urls.i18n')),
    url('^markdown/', include('django_markdown.urls')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^accounts/profile/', user_manager.views.login_page),
]

