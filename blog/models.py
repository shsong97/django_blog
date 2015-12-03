# -*- coding: utf-8 -*-

from django.db import models
import datetime
from django.utils import timezone
from django.contrib.auth.models import User
from django_markdown.models import MarkdownField
from django.core.urlresolvers import reverse
# Create your models here.

class Blog(models.Model):
    blog_title = models.CharField('Title',max_length=200)
    contents = MarkdownField() #models.TextField()
    pub_date = models.DateTimeField('Pub Date',default=timezone.now)
    user=models.ForeignKey(User)
    like_count = models.IntegerField('Like',default=0)
    view_count = models.IntegerField('View',default=0)
    
    def __unicode__(self):
        return self.blog_title
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <  now

    was_published_recently.admin_order_field = 'Pub Date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'recently published?'

    def get_absolute_url(self):
        return reverse('blog:detail',args=(self.id,))

    def serialize(self):
        data={
            'blog_id':self.id,
            'blog_title':self.blog_title,
            'pub_date':self.pub_date,
            'like_count':self.like_count,
            'username':self.user.username,
            'view_count':self.view_count,
            }
        return data

class Tag(models.Model):
    tag_title = models.CharField('Tag',max_length=100)
    blog = models.ManyToManyField(Blog)
    
    def __unicode__(self):
        return self.tag_title

# class BlogLike(models.Model):
#     blog = models.ManyToManyField(Blog)
#     user = models.ManyToManyField(User)