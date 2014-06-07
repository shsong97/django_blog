# -*- coding:utf-8 -*-
# Create your views here.
from django.http import HttpResponse,Http404
from django.template import Context, RequestContext
from django.template.loader import get_template
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib.auth import logout

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


def user_page(request,username):
    try:
        user=User.objects.get(username=username)
    except:
        raise Http404('사용자를 찾을수 없습니다.')
    
    bookmarks=user.bookmark_set.all()
#     template=get_template('user_page.html')
#     variables=Context({
#             'username':username,
#             'bookmarks':bookmarks
#         })
#     output=template.render(variables)
#     return HttpResponse(output)

    variables=RequestContext(request,{
            'username':username,
            'bookmarks':bookmarks            
        })
    return render_to_response('user_page.html',variables)

def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/bookmarks')

def registr_page(request):
    if request.method=='POST':
        form=RegistrationForm(request.POST)
        if form.is_valid():
            user=User.objects.create_user(
                username=form.cleaned_data['username']
                password=form.cleaned_data['password1']
                email=form.cleaned_data['email']
            )
            return HttpResponseRedirect('/bookmarks')
        else:
            form=RegistrationForm()
            
        variables=RequestContext(request,{'form':form})
        return render_to_response('registration/register.html',variables)