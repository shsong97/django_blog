# -*- coding: utf-8 -*-

from django.views import generic
from django.utils import timezone
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from blog.models import Blog
from django.core.urlresolvers import reverse
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required
import json
from django.views.generic.dates import YearArchiveView, MonthArchiveView
from django.db.models import Count
import datetime
# Create your views here.

login_url='/user/login'

class IndexView(generic.ListView):
    template_name = 'blog/blog_list.html'
    context_object_name = 'latest_blog_list'

    def get_queryset(self):
        """Return the last five published polls."""
        return Blog.objects.filter(
            pub_date__lte=timezone.now(),
        ).order_by('-pub_date')[:5]

class ShortIndexView(generic.ListView):
    template_name = 'blog/shortlist.html'
    context_object_name = 'latest_blog_list'

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

def blog_detail(request, pk):
    blog = get_object_or_404(Blog, id=pk)
    blog.view_count += 1
    blog.save()
    return render(request,'blog/detail.html',{'blog':blog})
    
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
        
    variables = {'title':title,
        'contents':contents
        }
    return render(request,'blog/add.html',variables)

def toJSON(objs, status=200):
    j=json.dumps(objs,ensure_ascii=False)
    return HttpResponse(j,status=status,content_type='application/json;charset=utf-8')

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
    return HttpResponseRedirect(reverse('blog:index'))

@login_required(login_url=login_url)
def blog_delete(request, blog_id):
    blogs = get_object_or_404(Blog,id=blog_id)
    if request.user == blogs.user:
        blogs.delete()
    return HttpResponseRedirect(reverse('blog:index'))

def blog_like(request, blog_id):
    blogs = get_object_or_404(Blog,id=blog_id)
    blogs.like_count = blogs.like_count+1
    blogs.save()
    data_dict={'result':blogs.like_count}
    return JsonResponse(data_dict)

def serialize(objs):
    serialized=[]
    for obj in objs:
        serialized.append(obj.serialize())
    return serialized
     
def blog_favorite(request):
    blog_list = Blog.objects.filter(user=request.user).order_by('-like_count')[:10]
    return JsonResponse(serialize(blog_list),safe=False)


class ArticleMonthArchiveView(MonthArchiveView):
    queryset = Blog.objects.all()
    date_field = "pub_date"
    allow_future = True
    # article.get_dated_queryset(**{'user__username':'shsong97'})
    # def get_dated_queryset(self, **lookup):
    #     return (super).get_dated_queryset(self, **lookup)

class ArticleYearArchiveView(YearArchiveView):
    queryset = Blog.objects.all()
    date_field = "pub_date"
    make_object_list = True
    allow_future = True
    
def blog_archive(request):
    blog_year = Blog.objects.filter(user=request.user).datetimes('pub_date','month').order_by('-pub_date')
    year_list=[]
    for current in blog_year:
        _year=current.year
        _month=current.month+1
        year_month=str(current.year)+'/'+str(current.month)
        
        if current.month==12:
            _year=current.year+1
            _month=1
        
        next_month=datetime.datetime(_year, _month, 1)
        count = Blog.objects.filter(
            user=request.user,
            pub_date__gte=current,
            pub_date__lt=next_month).aggregate(Count('pub_date'))
        
        year_list.append({'year':year_month,'count':count['pub_date__count']})

    return JsonResponse(year_list[:10],safe=False)