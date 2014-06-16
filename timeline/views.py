from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from timeline.models import *
from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import render_to_response
from django.template import RequestContext
import base64
import json

# Create your views here.
def serialize(objs):
    serialized=[]
    for obj in objs:
        serialized.append(obj.serialize())
    return serialized

def toJSON(objs, status=200):
    j=json.dumps(objs,ensure_ascii=False)
    return HttpResponse(j,status=status,content_type='application/json;charset=utf-8')

def need_auth(functor):
    def try_auth(request,*args,**kwargs):
        if 'HTTP_AUTHORIZATION' in request.META:
            basicauth=request.META['HTTP_AUTHORIZATION']
            user=None
        try:
            b64key=basicauth.split(' ')[1]
            key=base64.decodestring(b64key)
            (username,pw)=key.split(':')
        
            user=authenticate(username=username, password=pw)
        except:
            pass
        
        if user is not None:
            login(request,user)
            request.META['user']=user
            return functor(request,*args,**kwargs)

        logout(request)
        response=HttpResponse()
        response.status_code=401
#         response['WWW-Authenticate']='Basic '
        return response
    return try_auth
    
@need_auth
def timeline_view(request):
    messages=Message.objects.order_by('-created').all()
    ignore=request.user.userprofile.get_ignorelist()
    messages=messages.exclude(user__id__in=ignore)
    try:
        tweet_per_page=int(request.GET.get('per_page',10))
        page_num=int(request.GET.get('page',1))
        pages=Paginator(messages,tweet_per_page)
        resp = {
            'total_page': pages.num_pages,
            'total_count': pages.count,
            'messages': serialize(pages.page(page_num).object_list)
        }
        return toJSON(resp)
    except:
        resp = {
            'status':'pagination error'
        }
        return toJSON(resp,400)

def user_view(request,method):
    if method=='create' and request.method=='POST':
        try:
            username=request.POST.get('username')
            password=request.POST.get('password')
            if User.objects.filter(username__exact=username).count():
                return HttpResponse('duplicate id',400)
            user=User.objects.create_user(username,password=password)
            user.first_name=request.POST.get('name',)
            user.save()
            profile=UserProfile()
            profile.user=user
            profile.save()
            return toJSON({'status':'create suceess'})
        except:
            return toJSON({'status':'create fail'},400)

    elif method=='update' and request.method=='POST':
        try:
            username=request.POST.get('username')
            password=request.POST.get('oldpassword')
            newpassword=request.POST.get('newpassword')
            user=User.objects.get(username__exact=username)
            
            if user.check_password(password) is False:
                return toJSON({'status':'wrong password'},400)
            else:
                user.set_password(newpassword)
                user.first_name=request.POST.get('name',user.first_name)
                user.save()
        except:
            return toJSON({'status':'bad request'},400)
        return toJSON({'status':'updated'})
    elif method=='list' and request.method=='POST':
        users=UserProfile.objects.all()
        return toJSON(serialize(users))
    else:
        return toJSON({'status':'bad request'},400)
    
@need_auth
def message_create_view(request):
    if request.method != 'POST':
        return toJSON({'status':'bad request'},400)
    
    message=Message()
    try:
        message.user=request.user
        message.message=request.POST.get('message',)
        message.save()
        return toJSON({'status':'create success'})
    except:
        return toJSON({'status':'bad request'},400)
    
@need_auth
def message_view(request):
    try:
        message=Message.objects.get(id=num)
        return toJSON(message.serialize())
    except:
        return toJSON({'status':'not found'},400)
    
    return HttpResponse(None)

@need_auth
def message_delete_view(request,num):
    try:
        message=Message.objects.get(id=num)
        if message.user == request.user:
            message.delete()
            return toJSON({'status':'deleted'})
        else:
            return toJSON({'status':'forbidden'},401)
    except:
        return toJSON({'status':'not found'},400)
    
@need_auth
def like_view(request,num):
    try:
        message=Message.objects.get(id=num)
        like=Like()
        like.user=request.user
        like.message=message
        like.save()
    except:
        return toJSON({'status':'bad request'},400)
    
    return toJSON({'status':'created'})

@need_auth
def find_view(request):
    query=request.GET.get('query','')
    result=Message.objects.filter(Q(message__contains=query)|
                                 Q(user__userprofile__nickname__contains=query))
    return toJSON(serialize(result))

@need_auth
def name_view(request):
    if request.method == 'GET':
        data={
            'name':request.user.first_name,
        }
        return toJSON(data)
    if request.method == 'POST':
        try:
            name=request.POST.get('name')
            request.user.first_name=name
            request.user.save()
            return toJSON({'status':'updated'})
        except:
            return toJSON({'status':'bad request'},400)

@need_auth
def checkpassword_view(request):
    try:
        password=request.POST.get('password')
        if request.user.check_password(password):
            return toJSON({'status':'ok'})
    except:
        pass
    return toJSON({'status':'no'})

@need_auth
def setpassword_view(request):
    try:
        password=request.POST.get('password')
        if password:
            request.user.set_password(password)
            request.user.save()
            return toJSON({'status':'ok'})
    except:
        pass
        
    return toJSON({'status':'no'})

@need_auth
def profile_view(request,username=None):
    if username==None:
        username=request.user
    if request.method=='GET':
        try:
            userprofile=User.objects.get(username=username).userprofile
            return toJSON(userprofile.serialize())
        except:
            return toJSON({'status':'not found'},400)
        
    elif request.method=='POST':
        profile=request.user.userprofile
        profile.nickname=request.POST.get('nickname',profile.nickname)
        profile.comment=request.POST.get('comment',profile.comment)
        profile.country=request.POST.get('country',profile.country)
        profile.url=request.POST.get('url',profile.url)
        ignores=request.POST.get('ignore',None)
        if ignores:
            ignores=json.loads(ignores)
            profile.set_ignorelist(ignores)
            
        profile.save()
        
        return toJSON({'stauts':'updated'})
    
@need_auth
def login_view(request):
    return toJSON({'status':'ok','user':request.user.userprofile.serialize()})

def serve_html(request,page):
    load=page+".html"
    return render_to_response(load,{},context_instance=RequestContext(request))