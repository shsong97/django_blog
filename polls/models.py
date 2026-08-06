import datetime

from django.db import models
from django.utils import timezone


class PollList(models.Model):
    title = models.CharField('제목', max_length=200)
    pub_date = models.DateTimeField('등록일', default=timezone.now)
    start_date = models.DateField('시작일', default=timezone.now)
    end_date = models.DateField('종료일', default=timezone.now)

    POLL_STATUS = (
        ('OP', 'Open'),
        ('CL', 'Closed'),
    )

    status = models.CharField('상태', max_length=2, choices=POLL_STATUS, default='OP')

    def __str__(self):
        return self.title

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date < now

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = '최근등록일?'


class Poll(models.Model):
    poll_list = models.ForeignKey(PollList, on_delete=models.CASCADE)
    question = models.CharField('질문', max_length=200)
    total_count = models.IntegerField('전체투표수', default=0)

    def __str__(self):
        return self.question


class Choice(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice_text = models.CharField('선택항목', max_length=200)
    votes = models.IntegerField('투표수', default=0)

    def __str__(self):
        return self.choice_text
