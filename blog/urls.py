from django.conf.urls import patterns, url
from blog.views import *
from blog.feeds import RecentBlog

urlpatterns = patterns(
    '',
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^short/$', ShortIndexView.as_view(), name='short'),
    #url(r'^add/$', views.BlogCreate.as_view(), name='blog_add'), 
    url(r'^add/$', blog_addview, name='blog_add'),
    url(r'^favorite/$', blog_favorite, name='blog_favorite'),
    url(r'^feed/$', RecentBlog(), name='blog_feed'),
    url(r'^add/submit/$', blog_add, name='add_submit'),
    url(r'^(?P<pk>\d+)/$', blog_detail, name='detail'),
    url(r'^(?P<pk>\d+)/update/$', BlogUpdateView.as_view(), name='update'),
    url(r'^(?P<blog_id>\d+)/update/submit/$', blog_update, name='update_submit'),
    url(r'^(?P<blog_id>\d+)/delete/$', blog_delete, name='delete'),
    url(r'^(?P<blog_id>\d+)/like/$', blog_like, name='blog_like'),
    url(r'^archive/$', blog_archive, name='blog_archive'),
    url(r'^(?P<year>[0-9]{4})/$',
        ArticleYearArchiveView.as_view(),
        name="article_year_archive"),
    url(r'^(?P<year>[0-9]{4})/(?P<month>[0-9]+)/$',
        ArticleMonthArchiveView.as_view(month_format='%m'),
        name="archive_month_numeric"),
    url(r'^(?P<year>[0-9]{4})/(?P<month>[-\w]+)/$',
        ArticleMonthArchiveView.as_view(),
        name="archive_month"),        
) 
