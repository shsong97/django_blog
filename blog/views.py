from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import connection
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from django.views.generic.dates import MonthArchiveView, YearArchiveView

from blog.models import Blog

login_url = '/user/login/'


class BlogListView(ListView):
    template_name = 'blog/blog_list.html'
    context_object_name = 'latest_blog_list'

    def get_queryset(self):
        return Blog.objects.filter(
            pub_date__lte=timezone.now(),
        ).order_by('-pub_date')[:5]


class BlogDetailView(DetailView):
    model = Blog

    def get_object(self, queryset=None):
        blog = super().get_object(queryset)
        blog.view_count += 1
        blog.save(update_fields=['view_count'])
        return blog

    def get_queryset(self):
        return Blog.objects.filter(pub_date__lte=timezone.now())


class BlogDeleteView(LoginRequiredMixin, DeleteView):
    model = Blog
    success_url = reverse_lazy('blog:index')
    login_url = login_url


class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Blog
    fields = ['blog_title', 'contents']
    success_url = reverse_lazy('blog:index')
    login_url = login_url

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class BlogUpdateView(LoginRequiredMixin, UpdateView):
    model = Blog
    fields = ['blog_title', 'contents']
    login_url = login_url

    def form_valid(self, form):
        if not self.request.user.is_authenticated:
            return redirect(login_url)
        return super().form_valid(form)


def blog_like(request, blog_id):
    blogs = get_object_or_404(Blog, id=blog_id)
    blogs.like_count = blogs.like_count + 1
    blogs.save(update_fields=['like_count'])
    return JsonResponse({'result': blogs.like_count})


def serialize(objs):
    return [obj.serialize() for obj in objs]


def blog_favorite(request):
    blog_list = Blog.objects.all().order_by('-like_count')[:10]
    return JsonResponse(serialize(blog_list), safe=False)


class ArticleMonthArchiveView(MonthArchiveView):
    queryset = Blog.objects.all()
    date_field = 'pub_date'
    allow_future = True


class ArticleYearArchiveView(YearArchiveView):
    queryset = Blog.objects.all()
    date_field = 'pub_date'
    make_object_list = True
    allow_future = True


def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def blog_archive(request):
    vendor = connection.vendor
    if vendor == 'postgresql':
        query_str = """
            select date_part('year', pub_date) as year,
                   date_part('month', pub_date) as month,
                   count(*) as cnt
            from blog_blog
            group by date_part('year', pub_date), date_part('month', pub_date)
            order by 1 desc, 2 desc;
        """
    else:
        query_str = """
            select cast(strftime('%Y', pub_date) as integer) as year,
                   cast(strftime('%m', pub_date) as integer) as month,
                   count(*) as cnt
            from blog_blog
            group by year, month
            order by 1 desc, 2 desc;
        """
    with connection.cursor() as cursor:
        cursor.execute(query_str)
        year_list = dictfetchall(cursor)
    return JsonResponse(year_list, safe=False)
