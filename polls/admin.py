from django.contrib import admin

from polls.models import Choice, Poll, PollList


class ChoiceInline(admin.TabularInline):
    model = Choice
    verbose_name = '질문리스트'
    extra = 1


class PollAdmin(admin.ModelAdmin):
    fieldsets = [
        ('질문항목', {'fields': ['question']}),
        ('투표수', {'fields': ['total_count']}),
    ]
    inlines = [ChoiceInline]
    search_fields = ['question']
    list_display = ('poll_list', 'question', 'total_count')


class PollInLine(admin.TabularInline):
    model = Poll
    extra = 1


class PollListAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['title', 'status', 'start_date', 'end_date']}),
        ('등록일', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [PollInLine]
    list_filter = ['pub_date', 'start_date', 'end_date', 'status']
    search_fields = ['title', 'status']
    list_display = ('title', 'status', 'start_date', 'end_date', 'pub_date')


admin.site.register(Poll, PollAdmin)
admin.site.register(PollList, PollListAdmin)
