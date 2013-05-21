from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin

from .views import Home, About, Help


admin.autodiscover()


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns += patterns('',
    url('^$', Home.as_view(), name='home'),
    url('^about/$', About.as_view(), name='about'),
    url('^help/$', Help.as_view(), name='help'),

    url('^projects/', include('website.projects.urls')),
    url('^packages/', include('website.packages.urls')),
    url('^users/', include('website.users.urls')),
)
