# -.- coding: UTF-8 -.-
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import logout, login
from mysite.forms import RegistrationForm
from django.template import Context, RequestContext
from django.shortcuts import render_to_response, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import * 
from django.utils.http import is_safe_url
from django.contrib.auth.forms import *
from django.contrib.auth.decorators import login_required

# redirect login page

def home(request):
    return render(request,"index.html")

def test(request):
    form = PasswordResetForm()
    if form.is_valid():
        form.save()
    
    return render_to_response("test.html",RequestContext(request,{'form':form}))

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
    return HttpResponseRedirect('/login')

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
                
            return HttpResponseRedirect('/register/success/')
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
            print 'valid reset ?'
            form.save()
            return redirect('/')
    else:
        form=PasswordResetForm()
    temp_param='Reset Password'
    user_param={'form':form,'temp_param':temp_param}
    return render(request,'form_template.html',RequestContext(request,user_param))

@login_required
def user_profile_view(request, username):
    temp_param='View Profile'
    user_param={'username':username}
    return render(request,'form_template.html',RequestContext(request,user_param))