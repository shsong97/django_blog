from django.conf.urls import url
from blog.views import *
from blog.feeds import RecentBlog

urlpatterns = [
    url(r'^$', BlogListView.as_view(), name='index'),
    url(r'^add/$', BlogCreateView.as_view(), name='blog_add'),
    url(r'^(?P<pk>\d+)/$', BlogDetailView.as_view(), name='detail'),
    url(r'^(?P<pk>\d+)/update/$', BlogUpdateView.as_view(), name='update'),
    url(r'^(?P<pk>\d+)/delete/$', BlogDeleteView.as_view(), name='delete'),

    url(r'^(?P<blog_id>\d+)/like/$', blog_like, name='blog_like'),
    url(r'^favorite/$', blog_favorite, name='blog_favorite'),
    url(r'^feed/$', RecentBlog(), name='blog_feed'),
    url(r'^archive/$', blog_archive, name='blog_archive'),

    url(r'^list/(?P<year>[0-9]{4})/$',
        ArticleYearArchiveView.as_view(),
        name="article_year_archive"),
    url(r'^list/(?P<year>[0-9]{4})/(?P<month>[0-9]+)/$',
        ArticleMonthArchiveView.as_view(month_format='%m'),
        name="archive_month_numeric"),
    url(r'^list/(?P<year>[0-9]{4})/(?P<month>[-\w]+)/$',
        ArticleMonthArchiveView.as_view(),
        name="archive_month"),       
]
