# -*- coding: utf-8 -*-
from django.contrib.syndication.views import Feed
from blog.models import Blog
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.utils.feedgenerator import Atom1Feed

class RecentBlog(Feed):
    feed_type = Atom1Feed
    title=u'최신 블로그'
    link='/blog/feed/'
    description=u'최신 블로그 목록'
    
    def items(self):
        return Blog.objects.order_by('-id')[:10]
