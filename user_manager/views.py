from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.utils.translation import gettext_lazy as _

from user_manager.forms import RegistrationForm, ViewUserProfile


def contact(request):
    return render(request, 'contact.html')


def register_success(request):
    return render(request, 'registration/register_success.html')


def facebooklogin(request):
    return render(request, 'social_login.html')


def _safe_redirect_url(request, candidate, default='/'):
    if candidate and url_has_allowed_host_and_scheme(
        url=candidate,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        return candidate
    return default


def login_page(request):
    next_page = request.GET.get('next', '/')
    error_message = []

    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        next_page = request.POST.get('next', next_page)

        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(_safe_redirect_url(request, next_page))
            error_message.append(_('User is not acitve'))
        else:
            error_message.append(_('Id or password is wrong. Retry.'))

    return render(
        request,
        'registration/login.html',
        {'next': next_page, 'error_message': error_message},
    )


def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/user/login/')


def register_page(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
                email=form.cleaned_data['email'],
            )
            return HttpResponseRedirect('/user/register/success/')
    else:
        form = RegistrationForm()

    return render(
        request,
        'form_template.html',
        {'form': form, 'temp_param': 'Register'},
    )


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = PasswordChangeForm(user=request.user)

    return render(
        request,
        'form_template.html',
        {'form': form, 'temp_param': _('Change Password')},
    )


def reset_password(request):
    if request.method == 'POST':
        form = PasswordResetForm(data=request.POST)
        if form.is_valid():
            form.save(
                request=request,
                subject_template_name='registration/reset_subject.txt',
                email_template_name='registration/reset_email.html',
            )
            return render(request, 'registration/mail_send.html')
    else:
        form = PasswordResetForm()

    return render(
        request,
        'form_template.html',
        {'form': form, 'temp_param': _('Reset Password')},
    )


@login_required
def user_profile_view(request):
    temp_param = _('View Profile')
    form = ViewUserProfile(instance=request.user)

    if request.method == 'POST':
        form = ViewUserProfile(request.POST, instance=request.user)
        if form.is_valid():
            form.save()

    return render(
        request,
        'form_template.html',
        {'form': form, 'temp_param': temp_param},
    )
