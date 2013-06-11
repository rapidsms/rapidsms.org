from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin

from .views import About, Blogs, Help, Home


admin.autodiscover()


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns += patterns('',
    url(r'^scribbler/', include('scribbler.urls')),
)


urlpatterns += patterns('',
    url(r'^$', Home.as_view(), name='home'),
    url(r'^about/$', About.as_view(), name='about'),
    url(r'^blogs/$', Blogs.as_view(), name='blogs'),
    url(r'^help/$', Help.as_view(), name='help'),

    url(r'^projects/', include('website.projects.urls')),
    url(r'^packages/', include('website.packages.urls')),
    url(r'^users/', include('website.users.urls')),
)
