from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import patterns, include, url
from blog import views


urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    #url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name='detail'),
    #url(r'^(?P<pk>\d+)/results/$', views.ResultsView.as_view(), name='results'),
    #url(r'^(?P<blog_id>\d+)/vote/$', views.vote, name='vote'),
) 