from django.contrib import admin
from bookmarks.models import Tag, Bookmark, Link, SharedBookmark
from bookmarks.models import Friendship,Invitation
# Register your models here.
class AdminBookmark(admin.ModelAdmin):
    list_display=("title", "link", "user", )
    list_filter=("user",)
    ordering=("title",)
    search_fields=("title",)
    
admin.site.register(Bookmark, AdminBookmark)
admin.site.register(Tag)
admin.site.register(Link)
admin.site.register(SharedBookmark)
admin.site.register(Friendship,)
admin.site.register(Invitation,)