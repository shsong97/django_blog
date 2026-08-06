from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from polls.models import Choice, Poll, PollList


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_poll_list'

    def get_queryset(self):
        return PollList.objects.filter(
            pub_date__lte=timezone.now(),
            start_date__lte=timezone.now(),
            end_date__gte=timezone.now(),
        ).order_by('-pub_date')[:5]


class ShortIndexView(generic.ListView):
    template_name = 'polls/shortlist.html'
    context_object_name = 'latest_poll_list'

    def get_queryset(self):
        return PollList.objects.filter(
            pub_date__lte=timezone.now(),
            start_date__lte=timezone.now(),
            end_date__gte=timezone.now(),
        ).order_by('-pub_date')[:3]


class DetailView(generic.DetailView):
    model = PollList
    template_name = 'polls/detail.html'

    def get_queryset(self):
        return PollList.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = PollList
    template_name = 'polls/results.html'


def vote(request, poll_id):
    plist = get_list_or_404(Poll, poll_list=poll_id)
    polls = get_object_or_404(PollList, pk=poll_id)
    try:
        for p in plist:
            p_id = str(p.id)
            selected_choice = p.choice_set.get(pk=request.POST[p_id])
            selected_choice.votes += 1
            selected_choice.save(update_fields=['votes'])
            p.total_count += 1
            p.save(update_fields=['total_count'])
    except (KeyError, Choice.DoesNotExist):
        return render(
            request,
            'polls/detail.html',
            {
                'polllist': polls,
                'error_message': 'exists not selected items',
            },
        )
    return HttpResponseRedirect(reverse('polls:results', args=(poll_id,)))


def recent_poll(request):
    poll = (
        PollList.objects.filter(
            pub_date__lte=timezone.now(),
            start_date__lte=timezone.now(),
            end_date__gte=timezone.now(),
        )
        .order_by('-pub_date')
        .first()
    )
    if poll is None:
        return render(
            request,
            'polls/sub_poll.html',
            {
                'polllist': None,
                'poll_items': [],
            },
        )
    plist = get_list_or_404(Poll, poll_list=poll.id)
    return render(
        request,
        'polls/sub_poll.html',
        {
            'polllist': poll,
            'poll_items': plist,
        },
    )
