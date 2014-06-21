from django.conf.urls import patterns, include, url

from django.contrib import admin
from bookmarks.feeds import RecentBookmarks,UserBookmarks
from django.contrib.syndication.views import Feed
admin.autodiscover()

feeds = {
    'recent':RecentBookmarks,
    'user':UserBookmarks
}

urlpatterns = patterns(
    '',
    url(r'^$', 'mysite.views.home', name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^blog/', include('blog.urls',namespace="blog")),
    url(r'^polls/', include('polls.urls',namespace="polls")),
    url(r'^timeline/', include('timeline.urls',namespace="timeline")),
    url(r'^bookmarks/', include('bookmarks.urls',namespace="bookmarks")),
    url(r'^contact/', 'mysite.views.contact', name='contact'),
    # comments
    url(r'^comments/',include('django.contrib.comments.urls')),
    #url(r'^feeds/recent/$','django.contrib.syndication.views.Feed',RecentBookmarks ),  
    url(r'^feeds/(?P<url>.*)/$','django.contrib.syndication.views.Feed',{'feed_dict':feeds}),
    url(r'i18n/',include('django.conf.urls.i18n')),
)

