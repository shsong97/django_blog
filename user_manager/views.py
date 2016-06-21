# -.- coding: UTF-8 -.-
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect,HttpResponse

from django.contrib.auth import logout, login 
from django.contrib.auth.models import User
from django.contrib.auth.forms import * 
from django.contrib.auth.decorators import login_required

from django.utils.http import is_safe_url
from user_manager.forms import *
from django.core.urlresolvers import reverse
from django.contrib.auth.views import password_reset, password_reset_confirm
from django.utils.translation import gettext_lazy as _

def contact(request):
    return render(request,"contact.html")

def register_success(request):
    return render(request, 'registration/register_success.html')

def facebooklogin(request):
    return render(request, 'social_login.html')
    
def login_page(request):
    logout(request)
    username = password = ''
    next_page='/'
    error_message=[]
    if request.GET:
        next_page=request.GET.get('next','/')

    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                next_page = request.POST.get('next', '/')
                return HttpResponseRedirect(next_page)
            else:
                error_message.append(_('User is not acitve'))
        else:
            error_message.append(_('Id or password is wrong. Retry.'))
    return render(request, 'registration/login.html',{'next':next_page,'error_message':error_message})

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
                
            return HttpResponseRedirect('/user/register/success/')
    else:
        form=RegistrationForm()
            
    temp_param='Register'
    user_param={'form':form,'temp_param':temp_param}
    return render(request,'form_template.html',user_param)

@login_required
def change_password(request):
    if request.POST:
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = PasswordChangeForm(None) 
    temp_param=_('Change Password')
    user_param={'form':form,'temp_param':temp_param}
    return render(request,'form_template.html',user_param)

def reset_password(request):
    if request.POST:
        form=PasswordResetForm(data=request.POST)
        if form.is_valid():
            form.save(subject_template_name='registration/reset_subject.txt',
                      email_template_name='registration/reset_email.html',)
            return render(request,'registration/mail_send.html')
    else:
        form=PasswordResetForm()
    temp_param=_('Reset Password')
    user_param={'form':form,'temp_param':temp_param}
    return render(request,'form_template.html',user_param)

@login_required
def user_profile_view(request):
    temp_param=_('View Profile')
    if request.user:
        form=ViewUserProfile(instance=request.user)
        
    if request.POST:
        form=ViewUserProfile(request.POST,instance=request.user)
        if form.is_valid():
            form.save()

    user_param={'form':form,'temp_param':temp_param}
    return render(request,'form_template.html',user_param)