from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy

from user_manager import views

app_name = 'user_manager'

urlpatterns = [
    path('', views.login_page, name='login'),
    path('facebooklogin/', views.facebooklogin, name='facebooklogin'),
    path('login/', views.login_page, name='login_page'),
    path('logout/', views.logout_page, name='logout'),
    path('profile/', views.user_profile_view, name='profile'),
    path('register/', views.register_page, name='register'),
    path('register/success/', views.register_success, name='register_success'),
    path('changepassword/', views.change_password, name='change_password'),
    path('resetpassword/', views.reset_password, name='reset'),
    path(
        'password/reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='registration/reset_confirm.html',
            success_url=reverse_lazy('user_manager:reset_complete'),
        ),
        name='reset_confirm',
    ),
    path(
        'password/done/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='registration/reset_complete.html',
        ),
        name='reset_complete',
    ),
    path(
        'password/reset/done/',
        auth_views.PasswordResetDoneView.as_view(),
        name='reset_done',
    ),
]
