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
    (r'^charts/$', views.charts),
    (r'^charts/(\d+)/$', views.charts_brand),
    (r'^product/(\d+)/$', views.product),
    (r'^category/(\d+)/$', views.category),
    (r'^categories/$', views.categories),
    url(r'^search-form/$', views.search_form),
    url(r'^search/$', views.search),
    url(r'^datesearch/$', views.datesearch),
    url(r'^search_by_date/$', views.search_by_date),
    url(r'^custom/$', views.custom),
    url(r'^piebrand/$', views.piebrand),
    url(r'^piecategory/$', views.piecategory),
    url(r'^pie/$', views.pie_by_retailer),

)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()