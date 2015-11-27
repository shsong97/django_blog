# -*- coding: utf-8 -*-

from django.views import generic
from django.utils import timezone
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from blog.models import Blog
from django.core.urlresolvers import reverse
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required
from django.template import RequestContext

# Create your views here.

login_url='/user/login'

class IndexView(generic.ListView):
    template_name = 'blog/blog_list.html'
    context_object_name = 'latest_blog_list'
    taglist=[]
    
    def get_queryset(self):
        """Return the last five published polls."""
        return Blog.objects.filter(
            pub_date__lte=timezone.now(),
        ).order_by('-pub_date')[:5]

class ShortIndexView(generic.ListView):
    template_name = 'blog/shortlist.html'
    context_object_name = 'latest_blog_list'
    taglist=[]
    
    def get_queryset(self):
        """Return the last five published polls."""
        return Blog.objects.filter(
            pub_date__lte=timezone.now(),
        ).order_by('-pub_date')[:3]

class DetailView(generic.DetailView):
    model = Blog
    template_name = 'blog/detail.html'
    def get_queryset(self):
        return Blog.objects.filter(pub_date__lte=timezone.now())
    

class BlogUpdateView(generic.DetailView):
    model = Blog
    template_name = 'blog/update.html'

@login_required(login_url=login_url)
def blog_addview(request):
    title=''
    contents=''
    if request.POST:
        if request['title']:
            title=request['title']
        
        if request['contents']:
            contents=request['contents']
        
    variables=RequestContext(request,
        {'title':title,
        'contents':contents
        })
    return render_to_response('blog/add.html',variables)


@login_required(login_url=login_url)
def blog_update(request, blog_id):
    blogs = get_object_or_404(Blog,id=blog_id)
    blogs.blog_title=request.POST['blog_title']
    blogs.contents=request.POST['contents']
    blogs.save()
    return HttpResponseRedirect(reverse('blog:index'))

@login_required(login_url=login_url)
def blog_add(request):
    blogs = Blog(blog_title=request.POST['blog_title'],contents=request.POST['contents'],user=request.user,pub_date=timezone.now())
    blogs.save()
    return HttpResponseRedirect('/blog/')

@login_required(login_url=login_url)
def blog_delete(request, blog_id):
    blogs = get_object_or_404(Blog,id=blog_id)
    if request.user == blogs.user:
        blogs.delete()
    return HttpResponseRedirect('/blog/')

@login_required(login_url=login_url)
def blog_like(request, blog_id):
    blogs = get_object_or_404(Blog,id=blog_id)
    blogs.like_count = blogs.like_count+1
    blogs.save()
    return HttpResponseRedirect(reverse('blog:index'))