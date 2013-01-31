from django.conf.urls import patterns, include, url
from font_manager.views import Index, ViewFile, GetThumbnail
from django.http import HttpRequest
from django.conf import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'font_viewer.views.home', name='home'),
    # url(r'^font_viewer/', include('font_viewer.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$',Index),
    url(r'^thumbnail/(?P<path>.*)$','django.views.static.serve',{'document_root': settings.THUMBNAIL_FILE_PATH}),
    url(r'^download/(?P<path>.*)$','django.views.static.serve',{'document_root': settings.FONT_FILE_PATH}),
    url(r'^file/(?P<font_id>\d+)/$',ViewFile),
    url(r'^thumb/(?P<thumbnail_id>\d+)/$',GetThumbnail),

)
