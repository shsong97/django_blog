# -*- coding: utf-8 -*-
from django.contrib.syndication.views import Feed
from bookmarks.models import Bookmark
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.utils.feedgenerator import Atom1Feed

class RecentBookmarks(Feed):
    title=u'장고 북마크| 최신 북마크'
    link='/bookmarks/feed/recent/'
    description=u'장고 북마크 서비스를 통해서 등록된 북마크'
    
    def items(self):
        return Bookmark.objects.order_by('-id')[:10]

class UserBookmarks(Feed):
    feed_type = Atom1Feed
    def get_object(self, request, username):
        return User.objects.get(username=username)
    
    def title(self, user):
        return u'장고북마크|%s가 등록한 북마크' % user.username
    
    def link(self, user):
        return '/bookmarks/feed/user/%s/' % user.username
    
    def description(self, user):
        return u'장고 북마크 서비스를 통해서 %s가 등록한 북마크' % user.username
    
    def items(self, user):
        return user.bookmark_set.order_by('-id')[:10]