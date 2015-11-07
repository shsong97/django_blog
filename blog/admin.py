from django.contrib import admin
from blog.models import Blog, Tag, BlogLike
# Register your models here.
from django_markdown.admin import MarkdownModelAdmin

class AdminBlog(MarkdownModelAdmin):
    list_display=("blog_title", "pub_date", )
    list_filter=("pub_date",)
    ordering=("pub_date",)
    search_fields=("blog_title",)
    
admin.site.register(Blog,AdminBlog)
admin.site.register(Tag)
admin.site.register(BlogLike)