from django.conf.urls import include, url
from django.contrib.syndication.views import Feed
from django.contrib.auth.views import password_reset_done, password_reset_confirm, password_reset_complete
from user_manager import views

urlpatterns = [
    # user
    url(r'^$', views.login_page,name='login'),
    url(r'^facebooklogin/$', views.facebooklogin,name='facebooklogin'),
    url(r'^login/$', views.login_page,name='login'), # 'django.contrib.auth.views.login'
    url(r'^logout/$',views.logout_page),
    url(r'^profile/$',views.user_profile_view),
    url(r'^register/$',views.register_page),       
    url(r'register/success/$',views.register_success),
    url(r'^changepassword/$',views.change_password),
    url(r'^resetpassword/$', views.reset_password, name='reset'),
    url(r'^password/reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', password_reset_confirm,{'post_reset_redirect':'user_manager:reset_complete','template_name':'registration/reset_confirm.html'},name='reset_confirm'), 
    url(r'^password/done/$', password_reset_complete,{'template_name':'registration/reset_complete.html'},name='reset_complete'),
    url(r'^password/reset/done/$', password_reset_done,name='reset_done'),

]

