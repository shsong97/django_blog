from django.conf.urls import patterns, include, url

from django.contrib import admin
from bookmarks.feeds import RecentBookmarks,UserBookmarks
from django.contrib.syndication.views import Feed
from mysite import views
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
    # user
    url(r'^login/$', views.login_page), # 'django.contrib.auth.views.login'
    url(r'^accounts/login/$', views.login_page), # 'django.contrib.auth.views.login'
    url(r'^logout/$',views.logout_page),
    url(r'^profile/(\w+)$',views.user_profile_view),
    url(r'^register/$',views.register_page),       
    url(r'register/success/$',views.register_success),
    url(r'^changepassword/$',views.change_password),
    url(r'^resetpassword/$',views.reset_password),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm', name='password_reset_confirm'),
    url(r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete', name='password_reset_complete'),
    # test
    url(r'^test/$',views.test),
)

