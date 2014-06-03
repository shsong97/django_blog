from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'mysite.views.home', name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^blog/', include('blog.urls',namespace="blog")),
    url(r'^polls/', include('polls.urls',namespace="polls")),
    url(r'^timeline/', include('timeline.urls',namespace="timeline")),
    url(r'^contact/', 'mysite.views.contact', name='contact'),
)

