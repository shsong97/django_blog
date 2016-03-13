from django.conf.urls import include, url
from django.contrib import admin
from mysite import views

admin.autodiscover()

urlpatterns = [
    url(r'^$', 'mysite.views.home', name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^blog/', include('blog.urls',namespace="blog")),
    url(r'^polls/', include('polls.urls',namespace="polls")),
    url(r'^bookmarks/', include('bookmarks.urls',namespace="bookmarks")),
    url(r'^user/', include('user_manager.urls',namespace="user_manager")),
    url(r'^contact/', 'user_manager.views.contact', name='contact'),
    url(r'i18n/',include('django.conf.urls.i18n')),
    url('^markdown/', include('django_markdown.urls')),
    # test
    url(r'^test/$',views.test),
#     # user session
#     url(r'^accounts/password/reset/$', views.reset_password, name='password_reset'),
#     url(r'^accounts/password/reset/done/$', 'django.contrib.auth.views.password_reset_done',name='password_reset_done'),
#     url(r'^accounts/password/reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm', name='password_reset_confirm'),
#     url(r'^accounts/password/done/$', 'django.contrib.auth.views.password_reset_complete',name='password_reset_complete'),
]

