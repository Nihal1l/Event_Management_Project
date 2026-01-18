from django.contrib import admin
from django.urls import include, path
from debug_toolbar.toolbar import debug_toolbar_urls
from core.views import home, no_permission
from event_management import settings
from django.conf.urls.static import static
from django.conf import settings
from django.views.static import serve
from django.urls import re_path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('events/', include('events.urls')),
    path('users/', include('users.urls')),
    path('', home, name="home"),
    path('no-permission/', no_permission, name="no-permission")
] + debug_toolbar_urls()

urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]
