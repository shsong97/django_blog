# -.- coding: UTF-8 -.-
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import *

def home(request):
    return HttpResponseRedirect('/blog/')

def test(request):
    form = PasswordResetForm()
    if form.is_valid():
        form.save()
    
    return render(request, "test.html",{'form':form})
 
# def reset_password(request):
#     if request.POST:
#         form=PasswordResetForm(data=request.POST)
#         if form.is_valid():
#             form.save(subject_template_name='registration/password_reset_subject.txt',
#                       email_template_name='registration/password_reset_email.html',)
#             return render(request,'registration/mail_send.html')
#     else:
#         form=PasswordResetForm()
#     temp_param='Reset Password'
#     user_param={'form':form,'temp_param':temp_param}
#     return render(request,'form_template.html',RequestContext(request,user_param))