# -*- encoding:utf-8 -*-
from django import forms
import re
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _

class BookmarkSaveForm(forms.Form):
    url=forms.URLField(label='주소',widget=forms.TextInput(attrs={'size':64}))
    title=forms.CharField(label='제목',widget=forms.TextInput(attrs={'size':64}))
    tags=forms.CharField(label='태그',required=False,widget=forms.TextInput(attrs={'size':64}))
    share=forms.BooleanField(label='첫페이지에서 공유합니다.',required=False)
    
class SearchForm(forms.Form):
    query=forms.CharField(
        label='검색어를 입력하세요.',
        widget=forms.TextInput(attrs={'size':32}))

class FriendInviteForm(forms.Form):
    name=forms.CharField(label=_("Friend's name"))
    email=forms.EmailField(label=_("Friend's email"))
    
    