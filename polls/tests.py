import datetime

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from polls.models import PollList


class PollListMethodTests(TestCase):

    def test_was_published_recently_with_future_poll(self):
        future_poll = PollList(pub_date=timezone.now() + datetime.timedelta(days=30))
        self.assertEqual(future_poll.was_published_recently(), False)

    def test_was_published_recently_with_old_poll(self):
        old_poll = PollList(pub_date=timezone.now() - datetime.timedelta(days=30))
        self.assertEqual(old_poll.was_published_recently(), False)

    def test_was_published_recently_with_recent_poll(self):
        recent_poll = PollList(pub_date=timezone.now() - datetime.timedelta(hours=1))
        self.assertEqual(recent_poll.was_published_recently(), True)


def create_poll(title, days):
    now = timezone.now()
    return PollList.objects.create(
        title=title,
        pub_date=now + datetime.timedelta(days=days),
        start_date=(now + datetime.timedelta(days=min(days, 0))).date(),
        end_date=(now + datetime.timedelta(days=max(days, 1))).date(),
    )


class PollViewTests(TestCase):
    def test_index_view_with_no_polls(self):
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(response.context['latest_poll_list'], [])

    def test_index_view_with_a_future_poll(self):
        create_poll(title='Future poll.', days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(response.context['latest_poll_list'], [])


class PollIndexDetailTests(TestCase):
    def test_detail_view_with_a_future_poll(self):
        future_poll = create_poll(title='Future poll.', days=5)
        response = self.client.get(reverse('polls:detail', args=(future_poll.id,)))
        self.assertEqual(response.status_code, 404)

    def test_detail_view_with_a_past_poll(self):
        past_poll = create_poll(title='Past Poll.', days=-5)
        response = self.client.get(reverse('polls:detail', args=(past_poll.id,)))
        self.assertContains(response, past_poll.title, status_code=200)
