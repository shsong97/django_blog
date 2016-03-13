from django.conf.urls import url, include
from bookmarks import views
from bookmarks.feeds import RecentBookmarks,UserBookmarks

urlpatterns = [
    # bookmark search
    url(r'^$', views.main_page),
    url(r'^popular/$',views.popular_page,name='popular'),                   
    url(r'^user/(\w+)/$', views.user_page),

    # bookmark
    url(r'save/$',views.bookmark_save_page,name='save'),
    url(r'vote/$',views.bookmark_vote_page),
    url(r'tag/([^\s]+)/$',views.tag_page),
    url(r'tag/$',views.tag_cloud_page,name='tag_clouds'),
    url(r'taglist/$',views.tag_list),
    url(r'search/$',views.search_page,name='search'),
    url(r'bookmark/(\d+)/$',views.bookmark_page),
    url(r'^friends/(\w+)/$',views.friends_page),
    url(r'^friend/add/$',views.friend_add),
    url(r'^friend/invite/$',views.friend_invite,name='friend_invite'),
    url(r'^friend/accept/(\w+)/$',views.friend_accept),

    url(r'^feed/recent/$',RecentBookmarks(),name='feed_recent'),
    url(r'^feed/user/(\w+)/$',UserBookmarks(),name='feed_user'),
    
]
