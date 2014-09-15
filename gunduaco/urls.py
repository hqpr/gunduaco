from django.conf.urls import patterns, include, url

from django.contrib import admin
from products import views
from django.conf.urls import *
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf.urls import patterns, include, url
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^account/', include('account.urls')),
    url(r'^admin/', include(admin.site.urls)),
    (r'^account/', include('django.contrib.auth.urls')),
    (r'^accounts/', include('django.contrib.auth.urls')),
    (r'^charts/', views.price),

)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()