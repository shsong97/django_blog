# -*- coding: utf-8 -*-

from django.views import generic
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from blog.models import Blog
from django.core.urlresolvers import reverse

# Create your views here.

class IndexView(generic.ListView):
    template_name = 'blog/index.html'
    context_object_name = 'latest_blog_list'

    def get_queryset(self):
        """Return the last five published polls."""
        return Blog.objects.filter(
            pub_date__lte=timezone.now(),
        ).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Blog
    template_name = 'blog/detail.html'
    def get_queryset(self):
        return Blog.objects.filter(pub_date__lte=timezone.now())
    

class ResultsView(generic.DetailView):
    model = Blog
    template_name = 'blog/results.html'
    
def blog_update(request, blog_id):
    blogs = get_object_or_404(Blog,id=blog_id)
    blogs.title=request.POST['title']
    blogs.contents=request.POST['contents']
    blogs.save()
    return HttpResponseRedirect(reverse('blog:detail', args=(blog_id,)))
