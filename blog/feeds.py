# -*- coding: utf-8 -*-
from django.contrib.syndication.views import Feed
from blog.models import Blog
from django.utils.feedgenerator import Atom1Feed
from django.utils.translation import gettext_lazy as _

class RecentBlog(Feed):
    feed_type = Atom1Feed
    title=_('recent blog')
    link='/blog/feed/'
    description=_('list recent blog')
    
    def items(self):
        return Blog.objects.order_by('-id')[:10]
