# -*- coding:utf-8 -*-
# Create your views here.
from django.http import HttpResponse,Http404
from django.template import Context, RequestContext
from django.template.loader import get_template
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib.auth import logout 
# look method
# logout_then_login, password_change, 
# password_change_done, password_reset, password_reset_done
# redirect_to_login

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from bookmarks.models import Tag, Link, Bookmark, SharedBookmark
from bookmarks.forms import *
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime, timedelta

# redirect login page
login_url='/bookmarks/login'

def main_page(request):
    shared_bookmarks=SharedBookmark.objects.order_by('-date')[:10]
    variables=RequestContext(request,{'shared_bookmarks':shared_bookmarks})
    return render_to_response('main_page.html',variables)

def register_success(request):
    return render_to_response('registration/register_success.html',RequestContext(request))


def user_page(request,username):
    user=get_object_or_404(User,username=username)    
    bookmarks=user.bookmark_set.order_by('-id')

    variables=RequestContext(request,{
            'username':username,
            'bookmarks':bookmarks,
            'show_tags':True,
            'show_edit':username == request.user.username,
        })
    return render_to_response('user_page.html',variables)

def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')

def register_page(request):
    if request.method=='POST':
        form=RegistrationForm(request.POST)
        if form.is_valid():
            user=User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
                email=form.cleaned_data['email']
            )
            return HttpResponseRedirect('/bookmarks/register/success/')
    else:
        form=RegistrationForm()
            
    variables=RequestContext(request,{'form':form})
    return render_to_response('registration/register.html',variables)

def _bookmark_save(request,form):
    link, dummy = Link.objects.get_or_create(url=form.cleaned_data['url'])
    bookmark, created = Bookmark.objects.get_or_create(
        user=request.user,
        link=link
    )
    
    bookmark.title=form.cleaned_data['title']
    
    if not created:
        bookmark.tag_set.clear()
        
    tag_names=form.cleaned_data['tags'].split(',')
    for tag_name in tag_names:
        tag, dummy = Tag.objects.get_or_create(name=tag_name)
        bookmark.tag_set.add(tag)
    
    # 첫페이지에서 공유하도록 설정합니다.
    if form.cleaned_data['share']:
        shared_bookmark, created = SharedBookmark.objects.get_or_create(bookmark=bookmark)
    
    if created:
        shared_bookmark.users_voted.add(request.user)
        shared_bookmark.save()
        
    bookmark.save()
    return bookmark


# deco def : login_required : /accounts/login/
@login_required(login_url=login_url)
def bookmark_save_page(request):
    ajax=request.GET.has_key('ajax')
    if request.method=='POST':
        form=BookmarkSaveForm(request.POST)
        if form.is_valid():
            bookmark=_bookmark_save(request,form)
            if ajax:
                variables=RequestContext(request,{
                        'bookmarks':[bookmark],
                        'show_edit':True,
                        'show_tags':True
                    })
                return render_to_response('bookmark_list.html',variables)
            else:
                return HttpResponseRedirect('/bookmarks/user/%s/' % request.user.username)
        else:
            if ajax:
                return HttpResponse('failure')
    elif request.GET.has_key('url'):
        url=request.GET['url']
        title=''
        tags=''
        try:
            link=Link.objects.get(url=url)
            bookmark=Bookmark.objects.get(
                link=link,
                user=request.user
            )
            title=bookmark.title
            tags=','.join(
                tag.name for tag in bookmark.tag_set.all()
            )
        except ObjectDoesNotExist:
            pass
        form=BookmarkSaveForm({
            'url':url,
            'title':title,
            'tags':tags
        })
        
    else:
        form=BookmarkSaveForm()
    variables=RequestContext(request,{'form':form})    
    if ajax:
        return render_to_response('bookmark_save_form.html',variables)
    else:            
        return render_to_response('bookmark_save.html',variables)
    
def tag_page(request,tag_name):
    tag=get_object_or_404(Tag,name=tag_name)
    bookmarks=tag.bookmarks.order_by('-id')
    variables=RequestContext(request,{
            'bookmarks':bookmarks,
            'tag_name':tag_name,
            'show_tags':True,
            'show_user':True
        })
    return render_to_response('tag_page.html',variables)

def tag_cloud(request,htmlpage):
    MAX_WEIGHT=5
    tags=Tag.objects.order_by('name')
    
    min_count=max_count=tags[0].bookmarks.count()
    for tag in tags:
        tag.count=tag.bookmarks.count()
        if tag.count<min_count:
            min_count=tag.count
        if max_count<tag.count:
            max_count=tag.count
            
    range=float(max_count-min_count)
    if range==0.0:
        range=1.0
    for tag in tags:
        tag.weight=int(MAX_WEIGHT * (tag.count-min_count) / range )

    variables=RequestContext(request,{'tags':tags})
    return render_to_response(htmlpage,variables)


def tag_cloud_page(request):
    return tag_cloud(request,'tag_cloud_page.html')

def tag_list(request):
    return tag_cloud(request,'tag_list.html')

def search_page(request):
    form=SearchForm()
    bookmarks=[]
    show_results=False
    if request.GET.has_key('query'):
        show_results=True
        query=request.GET['query'].strip()
        if query:
            form=SearchForm({'query':query})
            bookmarks=Bookmark.objects.filter(title__icontains=query)[:10]
            
    variables=RequestContext(request,
                            {'form':form,
                             'bookmarks':bookmarks,
                             'show_results':show_results,
                             'show_tags':True,
                             'show_user':True
                            })
    if request.is_ajax():
        return render_to_response('bookmark_list.html',variables)
    else:
        return render_to_response('search.html',variables)

@login_required(login_url=login_url)
def bookmark_vote_page(request):
    if request.GET.has_key('id'):
        try:
            id=request.GET['id']
            shared_bookmark=SharedBookmark.objects.get(id=id)
            user_voted=shared_bookmark.users_voted.filter(username=request.user.username)
            if not user_voted:
                shared_bookmark.votes+=1
                shared_bookmark.users_voted.add(request.user)
                shared_bookmark.save()
        except ObjectDoesNotExist:
            raise Http404('북마크를 찾을수 없습니다.')
                
    if request.META.has_key('HTTP_REFERER'):
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    
    return HttpResponseRedirect('/bookmarks/') 

def popular_page(request):
    today=datetime.today()
    yesterday=today-timedelta(1)
    shared_bookmarks=SharedBookmark.objects.filter(date__gt=yesterday)
    shared_bookmarks=shared_bookmarks.order_by('-votes')[:10]
    variables=RequestContext(request,{
            'shared_bookmarks':shared_bookmarks
        })
    return render_to_response('popular_page.html',variables)

# def bookmark_page(request,bookmark_id):
#     shared_bookmark=get_object_or_404(SharedBookmark,id=bookmark_id)
#     variables=RequestContext(request,{
#             'shared_bookmark':shared_bookmark
#         })
#     return render_to_response('bookmark_page.html',variables)