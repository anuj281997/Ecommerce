
from django.contrib import admin
from django.urls import path,include,re_path
from django.views.static import serve

from . import settings
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('User.urls')),
    # re_path(r'^static/(?P<path>.*)$',serve,{'document_root': settings.STATIC_ROOT}),
]


urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = " AJ-Shop"
admin.site.site_title = "AJ-Shop"
admin.site.site_index_title = "Welcome To AJ-Shop"