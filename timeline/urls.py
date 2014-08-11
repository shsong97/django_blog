from django.conf.urls import patterns, url
from timeline import views

urlpatterns = patterns('',
    url(r'^api/timeline/$',views.timeline_view),
    url(r'^api/timeline/create/$',views.message_create_view),
    url(r'^api/timeline/(?P<num>\d+)/$',views.message_view),
    url(r'^api/timeline/(?P<num>\d+)/delete/$',views.message_delete_view),
    url(r'^api/timeline/(?P<num>\d+)/like/$',views.like_view),
    url(r'^api/timeline/find/$',views.find_view),                       
    url(r'^api/user/(?P<method>create)/$',views.user_view),
    url(r'^api/user/(?P<method>update)/$',views.user_view),
    url(r'^api/user/(?P<method>list)/$',views.user_view),
    url(r'^api/user/name/$',views.name_view),
    url(r'^api/user/checkpassword/$',views.checkpassword_view),
    url(r'^api/user/setpassword/$',views.setpassword_view),
    url(r'^api/profile/(?P<username>\w+)/$',views.profile_view),
    url(r'^api/profile/$',views.profile_view),
    url(r'^api/login/$',views.login_view),
    url(r'^(?P<page>\w+).html/$',views.serve_html),
)
