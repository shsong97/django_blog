import datetime

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Blog(models.Model):
    blog_title = models.CharField(_('Title'), max_length=200)
    contents = models.TextField(_('Contents'))
    pub_date = models.DateTimeField(_('Pub Date'), default=timezone.now)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    like_count = models.IntegerField(_('Like'), default=0)
    view_count = models.IntegerField(_('View'), default=0)

    def __str__(self):
        return self.blog_title

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date < now

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = _('recently published?')

    def get_absolute_url(self):
        return reverse('blog:detail', args=(self.id,))

    def serialize(self):
        return {
            'blog_id': self.id,
            'blog_title': self.blog_title,
            'pub_date': self.pub_date,
            'like_count': self.like_count,
            'username': self.user.username,
            'view_count': self.view_count,
        }


class Tag(models.Model):
    tag_title = models.CharField(_('Tag'), max_length=100)
    blog = models.ManyToManyField(Blog)

    def __str__(self):
        return self.tag_title
