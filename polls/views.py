# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404,get_list_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone
from polls.models import Choice, Poll,PollList

# Create your views here.

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_poll_list'

    def get_queryset(self):
        """Return the last five published polls."""
        return PollList.objects.filter(
            pub_date__lte=timezone.now(),
            start_date__lte=timezone.now(),
            end_date__gte=timezone.now()
        ).order_by('-pub_date')[:5]

class ShortIndexView(generic.ListView):
    template_name = 'polls/shortlist.html'
    context_object_name = 'latest_poll_list'

    def get_queryset(self):
        """Return the last five published polls."""
        return PollList.objects.filter(
            pub_date__lte=timezone.now(),
            start_date__lte=timezone.now(),
            end_date__gte=timezone.now()
        ).order_by('-pub_date')[:3]

class DetailView(generic.DetailView):
    model = PollList
    template_name = 'polls/detail.html'
    def get_queryset(self):
        """
        Excludes any polls that aren't published yet.
        """
        return PollList.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = PollList
    template_name = 'polls/results.html'

def vote(request, poll_id):
    # poll sub item list
    plist = get_list_or_404(Poll, poll_list=poll_id)
    # poll list
    polls = get_object_or_404(PollList,pk=poll_id)
    try:
        p_id=""
        # choice value validation
        for p in plist:
            p_id=str(p.id)
            selected_choice = p.choice_set.get(pk=request.POST[p_id])
        
        # if no error
        for p in plist:
            p_id=str(p.id)
            selected_choice = p.choice_set.get(pk=request.POST[p_id])
            selected_choice.votes += 1
            selected_choice.save()
            
            p.total_count += 1
            p.save()       
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the poll voting form.
        return render(request, 'polls/detail.html', {
            'polllist': polls,
            'error_message': "exists not selected items",
        })
    else:
        return HttpResponseRedirect(reverse('polls:results', args=(poll_id,)))

def recent_poll(request):
    poll = PollList.objects.filter(
            pub_date__lte=timezone.now(),
            start_date__lte=timezone.now(),
            end_date__gte=timezone.now()
        ).order_by('-pub_date')[0]
    plist = get_list_or_404(Poll, poll_list=poll.id)
    return render(request,'polls/sub_poll.html',{
            'poll',poll,
            'poll_items',plist,
        })

