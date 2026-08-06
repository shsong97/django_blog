from django.urls import path, re_path

from blog.feeds import RecentBlog
from blog.views import (
    ArticleMonthArchiveView,
    ArticleYearArchiveView,
    BlogCreateView,
    BlogDeleteView,
    BlogDetailView,
    BlogListView,
    BlogUpdateView,
    blog_archive,
    blog_favorite,
    blog_like,
)

app_name = 'blog'

urlpatterns = [
    path('', BlogListView.as_view(), name='index'),
    path('add/', BlogCreateView.as_view(), name='blog_add'),
    path('<int:pk>/', BlogDetailView.as_view(), name='detail'),
    path('<int:pk>/update/', BlogUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', BlogDeleteView.as_view(), name='delete'),
    path('<int:blog_id>/like/', blog_like, name='blog_like'),
    path('favorite/', blog_favorite, name='blog_favorite'),
    path('feed/', RecentBlog(), name='blog_feed'),
    path('archive/', blog_archive, name='blog_archive'),
    path('list/<int:year>/', ArticleYearArchiveView.as_view(), name='article_year_archive'),
    re_path(
        r'^list/(?P<year>[0-9]{4})/(?P<month>[0-9]+)/$',
        ArticleMonthArchiveView.as_view(month_format='%m'),
        name='archive_month_numeric',
    ),
    re_path(
        r'^list/(?P<year>[0-9]{4})/(?P<month>[-\w]+)/$',
        ArticleMonthArchiveView.as_view(),
        name='archive_month',
    ),
]
