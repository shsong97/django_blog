# -*- coding: utf-8 -*-

from django.db import models
import datetime
from django.utils import timezone

# Create your models here.

class Blog(models.Model):
    title = models.CharField('제목',max_length=200)
    contents = models.TextField()
    pub_date = models.DateTimeField('등록일',default=timezone.now())
    
    def __unicode__(self):
        return self.title
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <  now

    was_published_recently.admin_order_field = '등록일'
    was_published_recently.boolean = True
    was_published_recently.short_description = '최근등록일?'


class Tag(models.Model):
    tag_title = models.CharField('Tag',max_length=100)
    blog = models.ManyToManyField(Blog)
    
    def __unicode__(self):
        return self.tag_title