# -.- coding: UTF-8 -.-
from django.shortcuts import render,render_to_response, redirect
from django.template import Context, RequestContext
from django.http import HttpResponseRedirect,HttpResponse

from django.contrib.auth import logout, login 
from django.contrib.auth.models import User
from django.contrib.auth.forms import * 
from django.contrib.auth.decorators import login_required

from django.utils.http import is_safe_url
from user_manager.forms import *
from django.core.urlresolvers import reverse
from django.contrib.auth.views import password_reset, password_reset_confirm

def contact(request):
    return render(request,"contact.html")

def register_success(request):
    return render_to_response('registration/register_success.html',RequestContext(request))

def login_page(request):
    logout(request)
    username = password = ''

    if request.GET:
        print request.GET.get('next','/')
        next_page=request.GET.get('next','/')
        
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                next_page = request.POST.get('next', '/')
                print next_page
                return HttpResponseRedirect(next_page)
    return render_to_response('registration/login.html', context_instance=RequestContext(request))

def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/user/login')

def register_page(request):
    if request.POST:
        form=RegistrationForm(request.POST)
        if form.is_valid():
            user=User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
                email=form.cleaned_data['email']
            )
            if 'invitation' in request.session:
                invitation=Invitation.objects.get(id=request.session['invitation'])
                friendship=Friendship(from_friend=user,to_friend=invitation.sender)
                friendship.save()
                
                friendship=Friendship(from_friend=inviation.sender,to_friend=user)
                friendship.save()
                invitation.delete()
                del request.session['invitation']
                
            return HttpResponseRedirect('/user/register/success/')
    else:
        form=RegistrationForm()
            
    temp_param='Register'
    user_param={'form':form,'temp_param':temp_param}
    return render_to_response('form_template.html',RequestContext(request,user_param))

@login_required
def change_password(request):
    if request.POST:
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = PasswordChangeForm(None) 
    temp_param='Change Password'
    user_param={'form':form,'temp_param':temp_param}
    return render_to_response('form_template.html',RequestContext(request,user_param))

def reset_password(request):
    if request.POST:
        form=PasswordResetForm(data=request.POST)
        if form.is_valid():
#             form.save()
#             print form.as_p()
            form.save(subject_template_name='registration/reset_subject.txt',
                      email_template_name='registration/reset_email.html',)
            return render(request,'registration/mail_send.html')
    else:
        form=PasswordResetForm()
    temp_param='Reset Password'
    user_param={'form':form,'temp_param':temp_param}
    return render(request,'form_template.html',RequestContext(request,user_param))

@login_required
def user_profile_view(request):
    temp_param='View Profile'
    if request.user:
        form=ViewUserProfile(instance=request.user)
        
    if request.POST:
        form=ViewUserProfile(request.POST,instance=request.user)
        if form.is_valid():
            form.save()

    user_param={'form':form,'temp_param':temp_param}
    return render(request,'form_template.html',RequestContext(request,user_param))