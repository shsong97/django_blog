# -*- coding: utf-8 -*-

from django.views.generic import *
from django.views.generic.edit import *
from django.views.generic.dates import *
from django.utils import timezone
from django.shortcuts import *
from django.http import *
from blog.models import Blog
from django.core.urlresolvers import *
from django.contrib.auth.decorators import login_required
import json
from django.db.models import Count
import datetime 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import connection
# Create your views here.

login_url='/user/login/'

class BlogListView(ListView):
    template_name = 'blog/blog_list.html'
    context_object_name = 'latest_blog_list'
    def get_queryset(self):
        return Blog.objects.filter(
            pub_date__lte=timezone.now(),
        ).order_by('-pub_date')[:5]

class BlogDetailView(DetailView):
    model = Blog
    def get_queryset(self):
        return Blog.objects.filter(pub_date__lte=timezone.now())

class BlogDeleteView(LoginRequiredMixin, DeleteView):
    model = Blog
    success_url = reverse_lazy('blog:index')
    login_url=login_url

class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Blog
    fields=['user','blog_title','contents']
    success_url = reverse_lazy('blog:index')
    login_url=login_url

class BlogUpdateView(LoginRequiredMixin, UpdateView):
    model = Blog
    fields=['user','blog_title','contents']
    login_url=login_url
    def form_valid(self, form):
        if not self.request.user.username:
            return redirect(login_url)
        return super(UpdateView, self).form_valid(form)

def toJSON(objs, status=200):
    j=json.dumps(objs,ensure_ascii=False)
    return HttpResponse(j,status=status,content_type='application/json;charset=utf-8')

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
    blog_list = Blog.objects.all().order_by('-like_count')[:10]    
    return JsonResponse(serialize(blog_list),safe=False)

class ArticleMonthArchiveView(MonthArchiveView):
    queryset = Blog.objects.all()
    date_field = "pub_date"
    allow_future = True

class ArticleYearArchiveView(YearArchiveView):
    queryset = Blog.objects.all()
    date_field = "pub_date"
    make_object_list = True
    allow_future = True

def blog_archive(request):
    cursor=connection.cursor()
    cursor.execute("select date_part('year',pub_date) as year, date_part('month',pub_date) as month, count(*) as cnt from blog_blog group by date_part('year',pub_date),date_part('month',pub_date);")
    year_list = dictfetchall(cursor)
    print year_list
    return JsonResponse(year_list,safe=False)
def blog_archive2(request):
    blog_year = Blog.objects.all().datetimes('pub_date','month').order_by('-pub_date')
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
            pub_date__gte=current,
            pub_date__lt=next_month).aggregate(Count('pub_date'))
        year_list.append({'year':year_month,'count':count['pub_date__count']})
    # ArticleYearArchiveView.date_list
    return JsonResponse(year_list,safe=False)

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def test_sql(request):
    cursor = connection.cursor()
    row = dictfetchall(cursor)
    print row
