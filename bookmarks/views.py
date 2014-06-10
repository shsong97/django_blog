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
from bookmarks.models import Tag, Link, Bookmark
from bookmarks.forms import BookmarkSaveForm,RegistrationForm

# redirect login page
login_url='/bookmarks/login'



# method1 : get_template, Context usage
# def main_page(request):
#     template=get_template('main_page.html')
#     variables=Context({
#             'user':request.user
#         })
#     output=template.render(variables)
#     return HttpResponse(output)

# method2 : render_to_response (template, context)
# def main_page(request):
#     return render_to_response('main_page.html',{'user':request.user})

# method3 : render_to_response (template, requestcontext)
# requestcontext include request.user variable
def main_page(request):
    return render_to_response('main_page.html',RequestContext(request))

def register_success(request):
    return render_to_response('registration/register_success.html',RequestContext(request))


def user_page(request,username):
#     try:
#         user=User.objects.get(username=username)
#     except:
#         raise Http404('사용자를 찾을수 없습니다.')
    user=get_object_or_404(User,username=username)    
    bookmarks=user.bookmark_set.order_by('-id')
#     template=get_template('user_page.html')
#     variables=Context({
#             'username':username,
#             'bookmarks':bookmarks
#         })
#     output=template.render(variables)
#     return HttpResponse(output)

    variables=RequestContext(request,{
            'username':username,
            'bookmarks':bookmarks,
            'show_tags':True
        })
    return render_to_response('user_page.html',variables)

def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/bookmarks')

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

# deco def : login_required : /accounts/login/
@login_required(login_url=login_url)
def bookmark_save_page(request):
    if request.method=='POST':
        form=BookmarkSaveForm(request.POST)
        if form.is_valid():
            link, dummy = Link.objects.get_or_create(url=form.cleaned_data['url'])
            bookmark, created = Bookmark.objects.get_or_create(user=request.user,link=link)
            bookmark.title=form.cleaned_data['title']
            if not created:
                bookmark.tag_set.clear()
                
            tag_names=form.cleaned_data['tags'].split()
            for tag_name in tag_names:
                tag, dummy = Tag.objects.get_or_create(name=tag_name)
                bookmark.tag_set.add(tag)
                
            bookmark.save()
            return HttpResponseRedirect('/bookmarks/user/%s/' % request.user.username)
    else:
        form=BookmarkSaveForm()
            
    variables=RequestContext(request, { 'form':form })
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

def tag_cloud_page(request):
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
    return render_to_response('tag_cloud_page.html',variables)