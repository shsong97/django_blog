from django.conf.urls import patterns, url
from bookmarks import views
import os.path
site_media=os.path.join(os.path.dirname(__file__),'site_media')

urlpatterns = patterns('',
    url(r'^$', views.main_page),
    url(r'^user/(\w+)/$', views.user_page),
    url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^logout/$',views.logout_page),
    url(r'register/$',views.register_page),                       
) 
