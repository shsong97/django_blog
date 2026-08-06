from django.contrib import admin

from blog.models import Blog, Tag


@admin.register(Blog)
class AdminBlog(admin.ModelAdmin):
    list_display = ('blog_title', 'pub_date')
    list_filter = ('pub_date',)
    ordering = ('pub_date',)
    search_fields = ('blog_title',)


admin.site.register(Tag)
