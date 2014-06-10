from django.contrib import admin
from bookmarks.models import Tag, Bookmark, Link
# Register your models here.
admin.site.register(Bookmark)
admin.site.register(Tag)
admin.site.register(Link)