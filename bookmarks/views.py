# -*- coding:utf-8 -*-
# Create your views here.
from django.http import HttpResponse,Http404
from django.template import Context, RequestContext
from django.template.loader import get_template
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect

# look method
# logout_then_login, password_change, 
# password_change_done, password_reset, password_reset_done
# redirect_to_login

from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404
from bookmarks.models import Tag, Link, Bookmark, SharedBookmark, Friendship, Invitation
from bookmarks.forms import *
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime, timedelta

from django.db.models import Q
from django.core.paginator import Paginator

from django.utils.translation import gettext as _

ITEMS_PER_PAGE=10
login_url='/login'


def main_page(request):
    shared_bookmarks=SharedBookmark.objects.order_by('-date')[:10]
    variables=RequestContext(request,{'shared_bookmarks':shared_bookmarks})
    return render_to_response('main_page.html',variables)


def user_page(request,username):
    user=get_object_or_404(User,username=username)
    query_set=user.bookmark_set.order_by('id')
    paginator=Paginator(query_set,ITEMS_PER_PAGE)
    is_friend=Friendship.objects.filter(
        from_friend=request.user,
        to_friend=user
    )
    
    try:
        page=int(request.GET['page'])
    except:
        page=1
    try:
        bookmarks=paginator.page(page)
    except:
        raise Http404
        
    #bookmarks=user.bookmark_set.order_by('-id')

    variables=RequestContext(request,{
            'username':username,
            'bookmarks':bookmarks.object_list,
            'show_tags':True,
            'show_edit':username == request.user.username,
            'show_paginator':paginator.num_pages>1,
            'has_prev':bookmarks.has_previous(),
            'has_next':bookmarks.has_next(),
            'page':page,
            'pages':paginator.num_pages,
            'next_page':page+1, #bookmarks.next_page_number(),
            'prev_page':page-1, #bookmarks.previous_page_number(),
            'is_friend':is_friend
        })
    return render_to_response('user_page.html',variables)

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
    
    # share first page
    if form.cleaned_data['share']:
        shared_bookmark, created = SharedBookmark.objects.get_or_create(bookmark=bookmark)
    
        if created:
            shared_bookmark.users_voted.add(request.user)
            shared_bookmark.save()
        
    bookmark.save()
    return bookmark


# deco def : login_required : /accounts/login/
#@login_required(login_url=login_url)

# user permission
@permission_required('bookmarks.add_bookmark',login_url=login_url)
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
    
    min_count=max_count=0
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
    return tag_cloud(request,'taglist.html')

def search_page(request):
    form=SearchForm()
    bookmarks=[]
    show_results=False
    if request.GET.has_key('query'):
        show_results=True
        query=request.GET['query'].strip()
        if query:
            keywords = query.split()
            q=Q()
            for keyword in keywords:
                q = q & Q(title__icontains=keyword)
            form=SearchForm({'query':query})
            bookmarks=Bookmark.objects.filter(q)[:10]
            
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
            raise Http404('No bookmark.')
                
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

def bookmark_page(request,bookmark_id):
    shared_bookmark=get_object_or_404(SharedBookmark,id=bookmark_id)
    comments=CommentsForm()
    variables=RequestContext(request,{
            'shared_bookmark':shared_bookmark,
            'comments':comments
        })
    return render_to_response('bookmark_page.html',variables)

def friends_page(request, username):
    user=get_object_or_404(User, username=username)
    friends=[friendship.to_friend for friendship in user.friend_set.all()]
    friend_bookmarks=Bookmark.objects.filter(user__in=friends).order_by('-id')
    variables=RequestContext(request,{
            'username':username,
            'friends':friends,
            'bookmarks':friend_bookmarks[:10],
            'show_tags':True,
            'show_user':True
        })
    return render_to_response('friends_page.html',variables)

@login_required
def friend_add(request):
    if request.GET.has_key('username'):
        friend=get_object_or_404(User,username=request.GET['username'])
        friendship=Friendship(from_friend=request_user,to_friend=friend)
        try:
            friendship.save()
            request.user.message_set.create(
                message=u'%s is added' % friend.username
            )
        except:
            request.user.message_set.create(
                message=u'%s is already friend.' % friend.username
            )
        return HttpResponseRedirect('/bookmarks/friends/%s' % request.user.username )
    else:
        raise Http404
        
@login_required
def friend_invite(request):
    if request.method=='POST':
        form=FriendInviteForm(request.POST)
        if form.is_valid():
            invitation=Invitation(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                code=User.objects.make_random_password(20),
                sender=request.user
            )
            invitation.save()
            try:
                invitation.send()
                request.user.message_set.create(
                    message=_('An invitation was send to %s.') % invitation.email
                )
            except:
                request.user.message_set.create(
                    message=_('There was an error while sending the invitation.')
                )
            return HttpResponseRedirect('/bookmarks/friend/invite/')
    else:
        form=FriendInviteForm()
            
    variables=RequestContext(request,{'form':form})
    return render_to_response('friend_invite.html',variables)

def friend_accept(request, code):
    invitation=get_object_or_404(Invitation,code__exact=code)
    request.session['invitation']=invitation.id
    return HttpResponseRedirect('/register/')
