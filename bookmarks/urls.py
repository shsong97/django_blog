from django.conf.urls import patterns, url, include
from bookmarks import views
import os.path
# from django.views.generic.simple import direct_to_templates # ver 1.2


urlpatterns = patterns(
    '',
    # bookmark search
    url(r'^$', views.main_page),
    url(r'^popular/$',views.popular_page),                   
    url(r'^user/(\w+)/$', views.user_page),
    # session
    url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^logout/$',views.logout_page),
    url(r'^register/$',views.register_page),       
    url(r'register/success/$',views.register_success),
    # bookmark
    url(r'save/$',views.bookmark_save_page),
    url(r'vote/$',views.bookmark_vote_page),
    url(r'tag/([^\s]+)/$',views.tag_page),
    url(r'tag/$',views.tag_cloud_page),    
    url(r'taglist/$',views.tag_list),
    url(r'search/$',views.search_page),
    url(r'bookmark/(\d+)/$',views.bookmark_page),
    url(r'^friends/(\w+)/$',views.friends_page),
    url(r'^friend/add/$',views.friend_add),
    url(r'^friend/invite/$',views.friend_invite),
    url(r'^friend/accept/(\w+)/$',views.friend_accept),
) 
