# -*- coding: utf-8 -*-

from django.db import models
import datetime
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

class Blog(models.Model):
    blog_title = models.CharField('Title',max_length=200)
    contents = models.TextField()
    pub_date = models.DateTimeField('Pub Date',default=timezone.now())
    user=models.ForeignKey(User)
    like_count = models.IntegerField('Like',default =0)
    
    def __unicode__(self):
        return self.blog_title
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <  now

    was_published_recently.admin_order_field = 'Pub Date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'recently published?'


class Tag(models.Model):
    tag_title = models.CharField('Tag',max_length=100)
    blog = models.ManyToManyField(Blog)
    
    def __unicode__(self):
        return self.tag_title

class BlogLike(models.Model):
    blog = models.ManyToManyField(Blog)
    like_count = models.IntegerField('Like',default =0)