from django.conf import settings
from django.contrib import admin
from django.urls import include, path
import user_manager
from mysite import views

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('blog/', include(('blog.urls', 'blog'), namespace='blog')),
    path('polls/', include(('polls.urls', 'polls'), namespace='polls')),
    path('user/', include(('user_manager.urls', 'user_manager'), namespace='user_manager')),
    path('contact/', user_manager.views.contact, name='contact'),
    path('i18n/', include('django.conf.urls.i18n')),
    path('accounts/', include('allauth.urls')),
    path('accounts/profile/', user_manager.views.login_page),
]

if settings.DEBUG:
    try:
        import debug_toolbar
    except ImportError:
        debug_toolbar = None
    else:
        urlpatterns = [
            path('__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns
