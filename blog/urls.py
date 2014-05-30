from django.conf.urls import patterns, url
from blog import views


urlpatterns = patterns('',
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^add/$', views.BlogCreate.as_view(), name='blog_add'), 
    url(r'^add/submit/$', views.blog_add, name='add_submit'),
    url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^(?P<pk>\d+)/update/$', views.BlogUpdateView.as_view(), name='update'),
    url(r'^(?P<blog_id>\d+)/update/submit/$', views.blog_update, name='update_submit'),
    url(r'^(?P<blog_id>\d+)/delete/$', views.blog_delete, name='delete'),
) 
